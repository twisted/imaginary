package twisted.reality;
import java.util.Dictionary;
import java.util.Enumeration;
import java.util.Observer;
import java.util.Observable;
import java.util.Vector;
import twisted.util.StringLegalizer;
import twisted.util.AppendEnumeration;
import java.util.Date;
import java.io.PrintWriter;
import java.io.StringWriter;

/**
 * A Player object.	 This is the same as any other object, except
 * that it is connected to a user-interface which can be a real
 * honest-to-goodness human on the other end.
 * 
 * @see Thing 
 *
 * @version 1.0.0, 1 Jul 1999
 * @author Glyph Lefkowitz
 */

public class Player extends Location
{	
	RealityUI user;
	
	/**
	 * Creates a new Player object, in a specified location, with a
	 * specified String as the name, and a specified String as the
	 * description.
	 *
	 * @param inLoc The Thing's location 
	 *
	 * @param inName The Thing's name 
	 *
	 * @param inDesc The Thing's description
	 */	
	public Player(Location inLoc, String inName, String inDesc)
	{
		super(inLoc,inName,inDesc);
		password=new String();
	}
	
	/**
	 * Creates a new player with a name an a description, and places
	 * it at the default starting point for new players in the game.
	 *	
	 * @param b The name of the new Player.
	 *
	 * @param c The description of the new Player.	
	 */
	
	public Player(String b,String c)
	{
		this(null,b,c);
	}
	
	/**
	 * Creates a new Player object from no information at all.	This
	 * method is used when reading players from files.
	 */
	
	Player()
	{
		super();
	}
	
	/**
	 * Notifies the user that something has just entered the player's
	 * focus.
	 * @param th The thing that has just entered the room.
	 */
	
	void notifyEntered(Thing th)
	{
		if(user!=null && th!=this) user.notifyEntered(th, th.place());
	}
		
	/**
	 * Notifies the player that some object has exited their focus.
	 *
	 * @param th The thing that has left the room.
	 */
	
	void notifyLeft(Thing th)
	{
		if(user!=null && th!=this) user.notifyLeft(th, th.place());
	}
	
	/**
	 * Notifies the player that some object is about to exit their focus.
	 *
	 * @param th The thing which is leaving.
	 *
	 * @param str What it has to say about its departure.
	 */
	
	void notifyLeaving(Thing th, Object[] str)
	{
		if(user != null && th!=this) user.notifyLeaving(th, th.place(), fromMyPerspective(str));
	}
	
	/**
	 * Notifies the player that some object is about to enter their
	 * focus.
	 *
	 * @param th The thing which is entering.
	 *
	 * @param str What it has to say about its entrance.
	 */
	
	void notifyEntering(Thing th, Object[] str)
	{
		if(user != null && th!= this) user.notifyEntering(th, th.place(), fromMyPerspective(str));
	}
	
	/**
	 * Notifies the player that the description of the focus is
	 * being partially altered.
	 *
	 * @param theKey The identifier of the segment of the
	 * description which is being changed.
	 *
	 * @param theData What that segment of the description is being
	 * changed to.
	 */
	
	void notifyDescriptAppend(String theKey, Object theData)
	{
		if(user != null) user.notifyDescriptAppend(theKey,fromMyPerspective(theData));
	}
	
	/**
	 * Notifies a player that a part of the description is being removed.
	 *
	 * @param theKey The identifier of the segment of the
	 * description which is being changed.
	 */
	
	void notifyDescriptRemove(String theKey)
	{
		if(user != null) user.notifyDescriptRemove(theKey);
	}
	
	/**
	 * Locates the appropriate preposition; if I have one.
	 */
	
	String getPrepTo(Thing t)
	{
		String realPrep = getString("object preposition",t);
		if (realPrep == null)
		{
			realPrep = loc.getString("player preposition",t);
			if (realPrep == null)
			{
				realPrep = loc.getString("preposition",t);
				if (realPrep == null)
					realPrep="in";
			}
		}
		return realPrep;
	}
	
	/**
	 * This returns a string that displays in the client when this
	 * player is listed.  Rather than displaying the usual "there is a
	 * blah here" this will display "so-and-so is here".
	 */
	
	String isHereTo(Thing t)
	{
		StringBuffer sb;
		if ((loc != null) && (loc.isBroadcast()))
		{
			String realPrep = getPrepTo(t);
			return nameTo(t) + " is "+realPrep+" "+loc.the()+loc.nameTo(t)+((mood != null)?", "+mood+'.' : ".");
		}
		else
			return nameTo(t) + " is here" + ((mood!=null) ? ", "+mood+'.' : ".");
	}
	
	/**
	 * The name that is output when this player is written to file.
	 */
	
	String typeName()
	{
		return "Player";
	}
	
	/**
	 * Returns the content of the player's file persistance.
	 * Contains the player's superclass information (verbs, etc) and
	 * also abilities acquired by the player.
	 */
	
	public String content()
	{
		StringBuffer r = new StringBuffer(super.content());
		
		internalVerbList(r,abilities,"ability");
		
		if (isGod())
		{
			r.append("\n\tarchitect");
		}
		
		r.append("\n\tpasswd \"").append(StringLegalizer.legalize(password)).append("\"");
		
		return r.toString();
	}
	
	public synchronized void place(Location where)
	{
		super.place(where);
		if (user != null) user.notifyMoved();
	}
	
	/**
	 * Sets the user interface used by this player to a new user
	 * interface.  (The only currently available kind of interface is
	 * the NetClientUser, but it is concievable that in the future
	 * there will be a TelnetUser, or a WebUser)
	 *
	 * @param usr The user-interface to set.
	 */
	
	void setUI(RealityUI usr)
	{
		setUI(usr,null);
	}
	
	void setUI(RealityUI usr, Player toSwapTo)
	{
		if(user != null)
			user.attachToPlayer(toSwapTo);
		
		user = usr;
		
		if(usr!=null)
		{
			requests=dict();
			if (usr.who()!=this)
				usr.attachToPlayer(this);
			focusRefresh();
		}
		else
		{
			requests=null;
		}
	}
	
	/**
	 * Sets the current focus of the player to Thing th.
	 *
	 * @param th The thing to focus on.
	 */
	
	public void setFocus(Thing th)
	{
		if(myFocus != null) 
			myFocus.isNotObservedBy(this);
		myFocus = th;
		
		if(myFocus != null) 
			myFocus.isObservedBy(this);
		if(user!=null) 
			user.setFocus(th);
	}
	
	/**
	 * The current focus of this player (what the player is looking at).
	 */
	
	public Thing getFocus()
	{
		return myFocus;
	}
	
	/**
	 * A utility function.	This function returns an empty string.
	 * (because Players have proper names and aren't referred to as 'The James')
	 */
	
	String The()
	{
		return "";
	}
	
	/**
	 * A utility function.	This function returns an empty string.
	 * (because Players have proper names and aren't referred to as 'The James')
	 */
	
	String the()
	{
		return "";
	}
	
	/**
	 * Tells the user-interface to refresh the currently focused
	 * object.	Executed when something happens to the object that
	 * the player is looking at that indicates a change.
	 */
	
	void focusRefresh()
	{
		if(user != null) user.setFocus(myFocus);
	}
	
	Thing myFocus;
	
	/**
	 * Tests to see whether or not something is within the scope of
	 * the character.  That is, whether the player would be able to
	 * manipulate the object from where they stand.	 
	 *
	 * @param x The thing being tested.
	 */
	
	public boolean isWithinScope(Thing x)
	{
		Thing xloc = x.place();
		Thing xlocloc = (xloc == null)?null:xloc.place();
		return (
				(xloc == loc)    || 
				(xloc == this)   || 
				(xlocloc == loc) || 
				(xlocloc == this)
				);
	}
		
	/**
	 * After the planned rewrite of the client, this function will
	 * be used to indicate that the text is a response to a player's
	 * action. This should only be called from verbs that are
	 * responding to the player's typing.
	 * 
	 * <br>
	 * 
	 * However, for the time being, the only thing that happens here
	 * is a direct call of the "hears" method so don't expect any
	 * different behavior.
	 */
	public void respond(String s)
	{
		hears(s);
	}
	
	/**
	 * Causes the user to 'hear' a string.	Note, this is not
	 * literal audio.  It is merely a string displayed on the
	 * player's client.	 
	 *
	 * @param s The string to 'hear'.
	 */
	
	public void hears(String s)
	{
		if(user!=null) user.hears(String.valueOf(s));
	}
	
	/**
	 * This displays an alert to this player.  This is different from
	 * 'hears' in that it indicates that it ususally indicates that
	 * something has gone wrong, or something very important has
	 * happened.
	 */
	
	public void alert(String s)
	{
		user.errorMessage(s);
	}
	
	/**
	 * Causes the user to 'hear' a string.	Note, this is not
	 * literal audio.  It is merely a string displayed on the
	 * player's client.	 This function first evaluates all the
	 * Perceptibles by calling fromMyPerspective(s) on the array.
	 *
	 * @param s The array of Strings and Perceptibles to hear.
	 * 
	 * @see twisted.reality.Player#tellAll(twisted.reality.Thing, twisted.reality.Thing, java.lang.java.lang.Object[], java.lang.Object[])
	 */
	public void hears(Object[] s)
	{
		if(user!=null) user.hears(fromMyPerspective(s));
	}
	/**
	 * The same as hears(Object[]).  This converts the Vector to an
	 * array first, for convenience.
	 */
	public void hears(Vector v)
	{
		hears(fromVector(v));
	}
	
	
	private void addAmbiguity(String nm,
							   Location l,
							   twisted.util.LinkedList x)
	{
		try
		{
			Thing located = l.findThing(nm,this);
			if (located != null) 
			{
				x.addElement(located);
			}
		}
		catch (AmbiguousException ae)
		{
			Enumeration aeee = ae.elements();
			while(aeee.hasMoreElements())
			{
				x.addElement(aeee.nextElement());
			}
		}
	}
	
	/**
	 * Locates an object within the player's scope.
	 */
	
	public Thing locateThing (String s) throws AmbiguousException
	{
		if (s==null) return null;
		
		s=s.toLowerCase();
		Thing temptor=null;
		twisted.util.LinkedList ambig = new twisted.util.LinkedList();
		
		/* these are macros, they can never be ambiguous! */
		if (s.equals("me") || s.equals("self"))
			return this;
		if (s.equals("here"))
			return loc;
		if (s.equals("this"))
			return myFocus;
		
		Thing ths=null;
		
		if ( (myFocus != null) )
		{
			/* and this is *kinda* like a macro */
			String mfn = myFocus.name().toLowerCase();
			String MFN = myFocus.NAME().toLowerCase();
			if ( ((mfn == MFN) ? s.equals(mfn) : (s.equals(mfn)||s.equals(MFN)) )
				 || (myFocus.ll.get(s)!=null)
				 )
			{
				return myFocus;
			}
			
			if ( ( myFocus instanceof Location) && 
				 ( myFocus != place() ) && 
				 ( myFocus != topPlace() ) &&
				 ( myFocus != this ) )
			{
				addAmbiguity(s,(Location)myFocus,ambig);
			}
		}
		
		addAmbiguity(s,place(),ambig);
		addAmbiguity(s,topPlace(),ambig);
		addAmbiguity(s,this,ambig);
		
		if (ambig.size() <= 1)
		{
			return (Thing)ambig.elements().nextElement();
		}
		else
		{
			Enumeration whatWeGotWrong = ambig.elements();
			String nameToMe = ((Thing)whatWeGotWrong.nextElement()).nameTo(this);
			boolean itsAllTheSameToMe=true;
			// Does everything look the same to me?
			while (whatWeGotWrong.hasMoreElements())
			{
				if (!nameToMe.equals( ((Thing)whatWeGotWrong.nextElement()).nameTo(this)))
				{
					itsAllTheSameToMe=false;
					break;
				}
			}
			whatWeGotWrong=ambig.elements();
			if(itsAllTheSameToMe)
			{
				return (Thing)whatWeGotWrong.nextElement();
			}
			else
			{
				throw new AmbiguousException (whatWeGotWrong,s,this);
			}
		}
	}
	
	/**
	 * Gets an ability from the player.
	 *
	 * @param s The name of the ability to find.
	 *
	 * @return	the Verb associated with the ability, or null if the ability
	 *			is non-existant on this player.
	 */
	
	public final Verb getAbility(String x)
	{
		String c;
		// if this object has the ability x, get the class
		try
		{
			if(abilities != null && (c = (String)abilities.get(x)) != null)
				return Age.theUniverse().dynLoadVerb(c);
		} catch (ClassNotFoundException e) {
			Age.log("Error using Verb: " + e);
			return null;
		}

		// otherwise ask the super
		if(superclass != null && superclass.sThing() != null)
			return ((Player) superclass.sThing()).getAbility(x);
		
		// hm, no super, and no ability of that name here, return null
		return null;
	}
	
	/**
	 * This requests a response from the player.  A requested
	 * response is usually a window popped up on the user's client.
	 *
	 * @param r The response processor which will be notified when the
	 * request is responded to.
	 *
	 * @param s The prompting string.
	 *
	 * @param def The default text in the client window.
	 */
	
	public final void requestResponse(ResponseProcessor r, String s, String def)
	{
		if(requests == null) requests = dict();
		Long l = new Long((new Date()).getTime());
		if(r != null)
			requests.put(l,r);
		user.requestResponse(l,s,def);
	}
	
	/**
	 * Called when the player enters a response.
	 *
	 * @param s The string the player entered.
	 *
	 * @param l The key associated with this request.
	 */
	
	public final void gotResponse(String s, Long l)
	{
		
		ResponseProcessor rp = ((ResponseProcessor) requests.get(l));
		if (rp != null)
			rp.gotResponse(s);
		requests.remove(l);
	}
	
	/**
	 * Checks to see whether this player is trusted to perform God
	 * functions.
	 */
	
	public boolean isGod()
	{
		return godBit;
	}
	
	boolean godBit;
	
	/**
	 * Adds an ability verb to this player.
	 *
	 * @param v The ability to add.
	 * 
	 * @throws ClassNotFoundException if the class specified is not found.
	 */
	
	public final void addAbility(String vn) throws ClassNotFoundException
	{
		if(abilities == null) abilities=dict();
		internalEnable(vn,abilities);
	}
	
	/**
	 * Remove an ability from this player.
	 *
	 * @param s The key of the ability to remove.
	 */
	
	public final void removeAbility(String s) throws ClassNotFoundException
	{
		internalDisable(s,abilities);
		/* garbage collect unused tables */
		if (abilities.isEmpty())
			abilities=null;
	}
	
	/**
	 * Retrieves the user-interface object for this Player.
	 */
	
	RealityUI getUI()
	{
		return user;
	}
	
	/**
	 * Transfer control of this player to the user interface from
	 * another player.  This means that this player (which is not
	 * currently being controlled) gives control of itself to the
	 * given player.  The other player is logged out, and all actions
	 * of the user-interface of that player are now transferred to
	 * this one.
	 * 
	 * @param x The player to get the UI from.
	 */
	
	public void transferControlTo(Player x)
	{
		if ((x != null) && (x.getUI() != null))
		{
			RealityUI rx = x.getUI();
			x.setUI(null,this);
			Age.theUniverse().PLAYERS.put(this,this);
			setUI(rx);
			Age.theUniverse().PLAYERS.remove(x);
		}
	}
	
	/**
	 * Switch control of this player and another player, if both
	 * players are currently being controlled.  Otherwise, do nothing.
	 * 
	 */
	
	public void swapControlWith(Player x)
	{
		if (x!=null)
		{
			RealityUI rui = x.getUI();
			RealityUI mui = getUI();
			if ((rui != null) && (mui!=null))
			{
				setUI(rui,x);
				x.setUI(mui,this);
			}
		}
	}
	
	/**
	 * Determines whether or not this player is currently being
	 * controlled.
	 */
	
	public boolean isLoggedIn()
	{
		return getUI()!=null;
	}
	
	/**
	 * This causes a Player to do something, as if they had typed it
	 * in at a game interface window.
	 * 
	 * @param sentence The string that the player would have typed,
	 * such as "go north"
	 */
	
	public void execute(String sentence)
	{
		/* Hmm... nothing uses "password" except the login checker, so
		 * I won't waste another object for thread-locking (besides,
		 * you shouldn't be able to log in again while you're actually
		 * doing something)
		 */
		
		synchronized(password)
		{
			try
			{
				Sentence d = new Sentence(sentence,this);
				while(!d.sVerb().action(d));
			}
			catch(VerbHaltedException mvhe)
			{
				/* do nothing */
				/* -- TR 1.0 -- this should no longer be a problem. */
			}
			catch (RPException e)
			{
				hears(e.toString());
			}
			catch(Throwable e)
			{
				if (isGod())
				{
					StringWriter sw = new StringWriter();
					PrintWriter pw = new PrintWriter(sw);
					e.printStackTrace(pw);
					pw.flush();
					sw.close();
					hears("Unexpected error:\n"+sw.toString()); 
				}
				else
				{
					hears("An unexpected error occured at "+new Date()+": this is a bug!\nReport this time to the administrator of this game.");
					Age.log("Error Occurred to "+NAME());
					e.printStackTrace(System.out);
				}
			}
		}
	}
	
	/**
	 * Delay this player's input for a certain number of seconds.
	 */
	
	public void delay(int seconds)
	{
		if (user != null)
		{
			Thread ct = Thread.currentThread();
			Thread ut = user.getThread();

			if(ct==ut)
			{
				try
				{
					Thread.sleep(seconds*1000);
				}
				catch(InterruptedException inter)
				{
					Age.log("I just got an InterruptedException ("+inter+") in Player.delay.  Does this ever really happen?");
				}
			}
			else
			{
				user.askedWait = System.currentTimeMillis();
				user.waitFor = seconds * 1000;
			}
		}
	}
	
	/**
	 * This starts the CXHandler cx and its associated Clientside CX.
	 * 
	 * @param cx the CXHandler to start.
	 * @see twisted.reality.CXHandler
	 * @see twisted.reality.client.CX
	 */
	void startCX(CXHandler cx) throws RealClientException
	{
		user.startCX(cx);
	}
	String password;
	
	private Dictionary requests;
	private Dictionary abilities;
}
