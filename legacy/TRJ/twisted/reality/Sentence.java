package twisted.reality;
import java.util.StringTokenizer;
import java.util.Hashtable;
import java.io.StreamTokenizer;
import java.io.StringReader;
import java.util.Hashtable;
import java.util.Dictionary;
import java.util.Enumeration;
import java.util.NoSuchElementException;
import java.util.Vector;
import twisted.util.TRStringParser;
import twisted.util.QueueEnumeration;

/**
 * This is a representation of a sentence that a user types, such as
 * 'go north'.	Each piece of the sentence is represented by a
 * callable method in this object. For instance, in the sentence "take
 * hammer in bag on table with tongs", there is a direct object
 * (hammer), two indirect objects ('bag' and 'table'), and an abletive
 * object (tongs). Abletive objects are a grammatical idea stolen from
 * Latin, and while all of this is complete drivel linguistically
 * speaking, it gives one a fairly firm footing to begin analyzing a
 * sentence. You can set your verbs up with certain expectations
 * (i.e.: "Smite" will require a direct object, to be smitten) and
 * ignore possible errors, and the game will handle them for you.
 * (What do you want to smite?)	 The 'abletive object' hook is mostly
 * for verbs which are specifically geared to be done with a certain
 * object (kill troll with sword).
 *
 * @see Verb
 * @see Thing
 * 
 * @version 1.0.0, 1 Jul 1999
 * @author Glyph Lefkowitz
 */

public class Sentence
{
	class idorecord
	{
		public String string;
		public Thing thing;
		public String prep; 
	}
	
	/**
	 * A debugging macro.
	 */

	private void logAllParts()
	{
		
		Age.log("Sentence Logging");
		if (hasDirect())
			Age.log("directString="+directStr);
		if (hasDirectObject())
			Age.log("directThing="+directThing.NAME());
		
		Enumeration htob=indirectObjs.elements();
		Enumeration htky=indirectObjs.keys();
		while(htob.hasMoreElements())
		{
			idorecord ido = (idorecord) htob.nextElement();
			String str = (String) htky.nextElement();
			Age.log("indirectString(\""+str+"\")="+ido.string);
			if (ido.thing!=null)
				Age.log("indirectThing(\""+str+"\")="+ido.thing.NAME());
		}
		Age.log("Perpitrator="+perp);
	}
	
	static final int TT_STRING = 34;
	static final int TT_WORD = -3;
	static final int TT_NUMBER = -2;
	static final int TT_EOF = -1;
	static final int TT_EOL = '\n';
	
	/* This is here so the STUPID PoS Javadoc doesn't forget to make the index files...
	   It won't make them if any java file has a static initializer before a procedure.
	   Isn't that stupid?
	 */
	Sentence() {}
	
	static Hashtable preps;
	static Hashtable rmobs;
	static
	{
		preps = new Hashtable(20);
		//shortcuts = new Hashtable(20);
		rmobs = new Hashtable(20);
		
		/*
		 * TODO: there's gotta be some better, more modular way of
		 * doing this...  perhaps a default list of preps, then one
		 * that's modular to each verb?	 aaargghh... that's cyclic,
		 * more on this later
		 *
		 * NOTE: There are only 27 (or so) prepositions in the english
		 * language, and we're not going to be using them all...
		 *
		 * I can't wait for JDK 1.2 and HashMap...
		 * 
		 */
		
		preps.put("into","into");
		preps.put("in","in");
		preps.put("on","on");
		// preps.put("off","off");
		preps.put("to","to");
		preps.put("at","at");
		preps.put("from","from");
		preps.put("through","through");
		preps.put("except","except");
		preps.put("with","with");
		preps.put("by","by");
	}
	
	/** same as below ... but with abilities (yes, I am aware this is
        poor design, but it is a very small copy-and-paste.  If it
        gets much larger, it will have to be scrapped in favor of
        something more generic...) **/
	
	private boolean resolveA(Player toSearch,
							 boolean alreadyFound)
	{
		if (toSearch!=null)
		{
			Verb toUse=toSearch.getAbility(theVerbString);
			Verb toOverride=toSearch.getAbility("*");
			boolean ovt = (toOverride!=null);
			boolean ut = (toUse!=null);
			
			if (ovt)
			{
				possibleVerbs.enQueue(toOverride);
				possibleVerbThings.enQueue(toSearch);
			}
			
			if (ut)
			{
				possibleVerbs.enQueue(toUse);
				possibleVerbThings.enQueue(toSearch);
			}
			
			if (ut||ovt) return true;
		}
		return alreadyFound;
	}
	
	/**
	 * Enqueue one verb/thing pair and return whether or not they
	 * enqueued successfully (this is bizarrely structured to match
	 * the structure of the constructor)
	 */
	
	private boolean resolve(Thing toSearch,
							boolean alreadyFound)
	{
		if (toSearch!=null)
		{
			Verb toUse=toSearch.getVerb(theVerbString);
			Verb toOverride=toSearch.getVerb("*");
			boolean ovt = (toOverride!=null);
			boolean ut = (toUse!=null);
			
			if (ovt)
			{
				possibleVerbs.enQueue(toOverride);
				possibleVerbThings.enQueue(toSearch);
			}
			
			if (ut)
			{
				possibleVerbs.enQueue(toUse);
				possibleVerbThings.enQueue(toSearch);
			}
			
			if (ut||ovt) return true;
		}
		return alreadyFound;
	}
	
	private AmbiguousException ambiguity(AmbiguousException found)
		throws AmbiguousException
	{
		Enumeration aee = found.elements();
		while (aee.hasMoreElements())
		{
			if (((Thing)aee.nextElement()).getVerb(theVerbString)!=null)
				throw found;
		}
		return found;
	}
	
	
	boolean objsnotinited=true;
	
	/**
	 * Constructs a new sentence given a sentence string in the proper
	 * structure.  The format is: verb [direct object] [preposition
	 * indirect object] [preposition indirect object] ...  [ ("with"
	 * or "using") abletive object ]
	 *
	 * @param toparse The string to be parsed
	 * @param perp The perpetrator of the action
	 */
	
	Sentence(String toparse, Player perp) throws RPException
	{
		fullStr=toparse;
		String word;
		StringBuffer dobuf=null, wtsbuf=null;
		directStr="";
		indirectObjs = new Hashtable();
		this.perp=perp;
		boolean resolved=false;
		
		possibleVerbs = new QueueEnumeration();
		possibleVerbThings = new QueueEnumeration();
		try
		{
			TRStringParser st = new TRStringParser(toparse);
			word=theVerbString=(String)st.nextElement();
			
			Location pplace=perp.place();
			Location ptplace=perp.topPlace();
			Thing fcs=perp.getFocus();
			
			/* First override: your place. */
			resolved=resolve(pplace,resolved);
			
			/* Second override: if your top-place is different than
               your place, your top-place. */
			
			if (ptplace!=pplace)
				resolved=resolve(ptplace,resolved);
			
			/* Third override: if your focus is different than your
			   place and different than your top-place, */
			
			if ((ptplace != fcs) && (pplace != fcs))
				resolved=resolve(fcs,resolved);
				
			

			word=(String)st.nextElement();
			try
			{
				while(st.wasQuoted() || !preps.containsKey(word))
				{
					if(dobuf == null)
						dobuf = new StringBuffer(word);
					else
						dobuf.append(' ').append(word);
					// when we run out of elements, throws a
					// NoSuchElementException ... this is considered
					// normal, and so it's handled later
					word=(String)st.nextElement();
				}
			}
			finally
			{
				if (dobuf != null)
				{
					directStr = dobuf.toString();
					try
					{
						resolved=resolve
							(directThing=perp.locateThing(directStr),
							 resolved);
					}
					catch(AmbiguousException ambi)
					{
						_doe=ambiguity(ambi);
					}
				}
			}
			
			/* now we're going to go and get the indirect objects */
			while(preps.containsKey(word))
			{
				String preptmp = word;
				StringBuffer tempbuf=null;
				
				if (!st.hasMoreElements())
					throw new RPParseException
						("Pardon me, but "
						 + word + 
						 " what?  Please be more specific.");
				
				word=(String)st.nextElement();
				try
				{
					while(st.wasQuoted() || !preps.containsKey(word))
					{
						if(tempbuf == null)
							tempbuf = new StringBuffer(word);
						else
							tempbuf.append(' ').append(word);
						word=(String)st.nextElement();
					}
				}
				finally
				{
					//Age.log("done: "+ preptmp + ", " + itemp.string);
					idorecord itemp=new idorecord();
					
					itemp.string=tempbuf.toString();
					itemp.prep=preptmp;
					
					indirectObjs.put(preptmp, itemp);
					/*
					 * resolve indirect object
					 */
					try
					{
						itemp.thing=perp.locateThing(itemp.string);
						resolved=resolve(itemp.thing,resolved);
					}
					// At some point, I should look for verbs in here,
					// and revamp AmbiguousVerbException to give more
					// verbose error messages.
					catch(AmbiguousException ae)
					{
						putIOAE(preptmp,ambiguity(ae));
					}
				}
			}
		}
		catch (NoSuchElementException e)
		{
			// This is perfectly normal.  It means that parsing
			// halted, somewhere looking for a direct or indirect
			// object.
		}
		
		/*
		 * Now, if there isn't a verb candidate already, look for an
		 * object that has this verb that and set as a default verb.
		 * (remember to file a message when we do so!)
		 */

		if(!resolved)
		{
			// System.out.println("Didn't resolve, searching defaultprep...");
			twisted.util.AppendEnumeration e = new twisted.util.AppendEnumeration();

			e.append(place().things());
			e.append(perp.things());
			
			/*** if it is ever changed so that players are 'broadcast' by
	         *** default, CHANGE THIS ***/
			
			
			while (e.hasMoreElements() && !resolved)
			{
				Verb tmpvrb=null;
				/* temporary T */
				Thing temptee = (Thing) (e.nextElement());
				tmpvrb=temptee.getVerb(theVerbString);
				if ((tmpvrb!=null) && (tmpvrb.defaultPrep!=null))
				{
					if (tmpvrb.defaultPrep.equals(""))
					{
						/* we are operating on the direct object */
						if (!hasDirect())
						{
							directThing=temptee;
							directStr=temptee.name();
							possibleVerbs.enQueue(tmpvrb);
							possibleVerbThings.enQueue(temptee);
							resolved=true;
						}
						/* otherwise don't bother ... the client has
						   already told us what directobject we should
						   be using */
					}
					else if (!hasIndirect(tmpvrb.defaultPrep))
					{
						idorecord bloop = new idorecord();
						
						bloop.thing = temptee;
						bloop.string = temptee.name();
						bloop.prep = tmpvrb.defaultPrep;
						
						indirectObjs.put(tmpvrb.defaultPrep,bloop);
						possibleVerbs.enQueue(tmpvrb);
						possibleVerbThings.enQueue(temptee);
						resolved=true;
					}
					
					/* if I resolved it on this pass */
					if (resolved)
					{
						defaultedPrep=tmpvrb.defaultPrep;
						
						// inform the user that they've just been
						// automatically forwarded to a provided
						// preposition
						Object[] zorf =
						{
							"(",
							tmpvrb.defaultPrep,
							(tmpvrb.defaultPrep.equals(""))?"":" ",
							temptee,
							")"
						};
						appendResponse(zorf);
					}
				}
			}
		}
		
		// The player is absolutely the last thing that gets considered.
		
		resolved=resolveA(perp,resolved);
		
		if (!resolved)
			throw new NoSuchVerbException(theVerbString);

		// logAllParts();
	}
	
	/**
	 * If a 'defaulted' verb returns false (one that has a
	 * defaultPrep) this function will re-set the sentence so that it
	 * does not have the defaulted components (direct/indirect
	 * object/string) so the other verbs won't get incorrect data.
	 */
	
	private void resetDefaulted()
	{
		if (defaultedPrep != null)
		{
			if (defaultedPrep.equals(""))
			{
				directThing=null;
				_doe=null;
				directStr=null;
			}
			else
			{
				indirectObjs.remove(defaultedPrep);
			}
		}
	}
	
	private Thing xObject(String name,
						  Thing thing,
						  AmbiguousException except,
						  RPException rpe)
						  
						  throws RPException
	{
		if(thing != null)
		{
			return thing;
		}
		else if (except != null)
		{
			throw except;
		}
		else if (name!=null && !name.equals(""))
		{
			String ntlc=name.toLowerCase();
			String ppdt=perp.getFocus().fullyDescribeTo(perp).toLowerCase();
			
			if (ppdt.indexOf(ntlc)!=-1)
			{
				throw new NotInterestingException (ntlc,theVerbString);
			}
			else
			{
				throw new NoSuchThingException(name);
			}
		}
		throw rpe;
	}
		
	private void putIOAE(String ionm, AmbiguousException ae)
	{
		if (_ioe==null) _ioe=new twisted.util.LinkedList();
		_ioe.put(ionm,ae);
	}
	
	private AmbiguousException getIOAE(String ionm)
	{
		if(_ioe==null) return null;
		return (AmbiguousException) _ioe.get(ionm);
	}
	
	/**
	 * This returns the next verb in the sequence of verbs that this
	 * Sentence located as possibly appropriate.  It also performs
	 * some housekeeping.
	 */
	
	Verb sVerb() throws RPException
	{
		if (theVerb != null)
		{
			playerResponse=null;
			resetDefaulted();
		}
		theVerb = (Verb) possibleVerbs.nextElement();
		theVerbThing = (Thing) possibleVerbThings.nextElement();
		if (theVerb == null)
			throw new NoSuchVerbException (theVerbString);
		return theVerb;
	}
	
	/**
	 * Appends a response to the player that will be sent (when???
	 * right now its sent when subject gets called...  that seems
	 * kinda hacky to me.)  Right now this seems to only be used to
	 * inform the player that they are using a default object. Is this
	 * public for a reason?  */
	
	void appendResponse(Object[] strng)
	{
		if (playerResponse==null)
		{
			playerResponse=new Vector();
		}
		else
		{
			playerResponse.addElement("\n");
		}
		for(int i = 0; i < strng.length; i++)
		{
			playerResponse.addElement(strng[i]);
		}
	}
	
	/**
	 * The direct object, as a Thing.  This is usually the word
	 * immediately following the verb.	This is not always what you
	 * want to use, though - for instance, in the sentence "say
	 * hello", "hello" is not a Thing -- in such a case, you would
	 * rather use <code>directString();</code>'.
	 *
	 * @return A Thing representing the direct object.
	 */
	
	public Thing directObject() throws RPException
	{
		return xObject(directStr,directThing,_doe,new NoDObjectException(theVerbString));
	}

	/**
	 * The direct object, as a String.
	 */
	
	public String directString() throws NoDObjectException
	{
		if(!hasDirect()) throw new NoDObjectException(theVerbString);
		return directStr;
	}

	/**
	 * Returns whether or not the user typed in a String that fits
	 * into the direct object.
	 */
	
	public boolean hasDirect()
	{
		return (directStr != null && !directStr.equals(""));
	}
	
	/**
	 * This function tells you if the directObject specified is a
	 * valid reference to a Thing that this player can see. If the
	 * object is not valid, or if the user didn't specify a direct
	 * object, this will return false.
	 */
	
	public boolean hasDirectObject()
	{
		return ((directThing!=null) ? true :(_doe!=null));
	}
	
	/**
	 * An indirect object in this Sentence, as a Thing.
	 *
	 * @param preposition The preposition of the indirect object that
	 * you're looking for.
	 * Acceptable prepositions are:
	 * <ul>
	 * <li> into
	 * <li> in
	 * <li> on
	 * <li> to
	 * <li> at
	 * <li> from
	 * <li> through
	 * <li> except
	 * <li> with
	 * </ul>
	 */
	
	public Thing indirectObject(String preposition) throws RPException
	{
		Object o = indirectObjs.get(preposition);
		Thing t=null;
		String s=null;
		if(o!=null)
		{
			t = ((idorecord) o).thing;
			s = ((idorecord) o).string;
		}
		
		return xObject(s,t,getIOAE(preposition),new NoIObjectException(theVerbString,preposition));
	}
	
	/**
	 * An indirect object in this Sentence, as a String.  
	 *
	 * @param preposition The preposition of the indirect object
	 * that you're looking for.
	 *
	 * Acceptable prepositions are:
	 * <ul>
	 * <li> into
	 * <li> in
	 * <li> on
	 * <li> to
	 * <li> at
	 * <li> from
	 * <li> through
	 * <li> except
	 * <li> with
	 * </ul>
	 */
	
	public String indirectString(String preposition) throws RPException
	{
		idorecord o = (idorecord) (indirectObjs.get(preposition));
		String s = (o==null) ? null: o.string;
		if(s==null) throw new NoIObjectException(theVerbString,preposition);
		return s;
	}
		
	/**
	 * Returns whether or not the user typed in a String that fits
	 * into the indirect object specified by the preposition given.
	 *
	 * @param s The preposition.
	 */
	
	public boolean hasIndirect(String s)
	{
		return (indirectObjs.get(s)!=null);
	}
	
	/**
	 * Returns whether or not the user specified a valid and present
	 * Thing in the indirect object specified by the given
	 * preposition.
	 * 
	 * @param s The preposition.
	 */
	
	public boolean hasIndirectObject(String s)
	{
		if(getIOAE(s)!=null) return true;
		Object o = indirectObjs.get(s);
		if((o==null)) return false;
		if( ((idorecord) o).thing==null) return false;
		return true;
	}

	/**
	 * Returns the Thing that the verb being executed was found on.
	 */
	public Thing verbObject()
	{
		return theVerbThing;
	}
	
	/**
	 * Returns the preposition that the verbObject was found with. 
	 */
	public String verbPreposition()
	{
		Enumeration ios = indirectObjs.elements();
		while (ios.hasMoreElements())
		{
			idorecord current = (idorecord) ios.nextElement();
			if (current.thing == verbObject())
			{
				return current.prep;
			}
		}
		return null;
	}
	
	/**
	 * This returns the Location wherein action is transpiring (if the subject
	 * is sitting in a chair, for example, it will return the room the chair
	 * is in)
	 *
	 * @return the location that the action transpires in
	 */
	
	public Location place()
	{
		return perp.topPlace();
	}
	
	/**
	 * Returns the player who is executing the verb.
	 */
	
	public Player subject()
	{
		if(!responseFlushed)
		{
			responseFlushed=true;
			if (playerResponse != null)
			{
				Object[] copied = new Object[playerResponse.size()];
				playerResponse.copyInto(copied);
				perp.hears(copied);
			}
		}
		// Okay, now if THIS is null, you've got problems.
		return perp;
	}
	
	/**
	 * Gets the verb the user entered as a string.
	 */
	
	public String verbString()
	{
		return theVerbString;
	}
	
	/**
	 * Returns the indirect object after 'with'.
	 * @depreciated use indirectObject("with") instead.
	 */
	
	public Thing withObject() throws RPException
	{
		return indirectObject("with");
	}

	/**
	 * Returns the indirect object after 'with' as a string.
	 * @depreciated use indirectString("with") instead.
	 */
	
	public String withString() throws RPException
	{
		return indirectString("with");
	}
	
	/**
	 * Returns whether the user specified a with clause.
	 * @depreciated use hasIndirect("with") instead.
	 */
	public boolean hasWith()
	{
		return hasIndirect("with");
	}

	/**
	 * Returns whether or not there is a real and present Thing
	 * as a "with" indirect object.
	 * @depreciated use hasIndirectObject("with") instead.
	 */
	  
	public boolean hasWithObject()
	{
		return hasIndirectObject("with");
	}
	
	/**
	 * This will give you the full, unparsed String that the verb came
	 * as.  If it is possible to avoid using this (which it usually
	 * is) please do so.  It is expensive and difficult to process the
	 * input in this way, and the engine already does as much as
	 * possible of it for you.
	 */
	
	public String fullString()
	{
		return fullStr;
	}
	
	private QueueEnumeration possibleVerbs;
	private QueueEnumeration possibleVerbThings;
	Vector playerResponse;
	boolean responseFlushed=false;
	AmbiguousException _doe;
	private twisted.util.LinkedList _ioe;
	
	String defaultedPrep;
	
	boolean triedDirect;
	boolean triedIndirect;
	boolean triedLocation;
	boolean triedPlayer;
	
	String		fullStr;
	String		directStr;
	Thing		directThing;
	String		theVerbString;
    Hashtable 	indirectObjs;
	Verb		theVerb;
	Thing		theVerbThing;
	
	Player	perp;
}
