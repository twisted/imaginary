package twisted.reality;

import java.util.Dictionary;
import java.util.Enumeration;
import twisted.util.EmptyEnumeration;
import twisted.util.ReverseClassEnumeration;
import twisted.util.ClassBasedEnumeration;

/**
 * This represents a place where a Thing can be.  Players and Rooms
 * are both Locations, and can "contain" objects.  It is not named
 * "container" because that would be misleading: a chair or a person,
 * both locations, are not containers.
 * 
 * @version 1.0.0, 1 Jul 1999
 * @author Glyph Lefkowitz
 */

public class Location extends Thing
{
	/**
	 * Creates a new Location.
	 * @param a The location of this location (usually null)
	 * @param b The name of this location
	 * @param c The description of this location.
	 */
	public Location(Location a, String b, String c)
	{
		super(a,b,c);
	}
	
	/**
	 * Creates a new Location, completely blank.  Please name and
	 * place a location created in this manner! This constructor is
	 * mainly used only for reading from a file.
	 */
	
	Location()
	{
		super();
	}

	private boolean broadcast=false;
	
	String thingIsHereTo(Thing t)
	{
		return super.isHereTo(t);
	}
	
	public synchronized void place(Location l)
	{
		if (broadcast /* && inventory != null ? */ )
		{
			removeAllFromParentView();
			if (contentsOperable)
				makeThisAllGoAway(true);
			super.place(l);
			if (contentsOperable)
				makeThisAllGoAway(false);
			addAllToParentView();
			Enumeration plr = players(true);
			if (plr!=null && l != null)
			{
				while (plr.hasMoreElements())
				{
					Player p = (Player) plr.nextElement();
					p.setFocus(l);
				}
			}
		}
		else
		{
			super.place(l);
		}
	}
	
	/**
	 * First puts everything where it was, then goes away.
	 */
	
	public void dispose()
	{
		Enumeration e = things(true,true);
		while (e.hasMoreElements())
		{
			Thing t = (Thing) e.nextElement();
			t.setComponent(false);
			t.place(place());
		}
		super.dispose();
	}
	
	/**
	 * Refreshes the item list of all things observing this object.
	 */
	public void itemRefreshMyObservers()
	{
		/* there should be a more efficient way of doing this
		 */
		focusRefreshMyObservers();
	}
	
	/**
	 * This changes the "broadcast" status of this Location. (whether or
	 * not objects are visible from the room)
	 * Should really use properties, not a dedicated bit.
	 * This is going away as soon as Glyph fixes it. :)
	 */
	
	public void setBroadcast(boolean inBroadcast)
	{
		if(broadcast != inBroadcast)
		{
			broadcast=inBroadcast;
			if (broadcast)
			{
				setContentsVisible(true);
				
				addAllToParentView();
			}
			else
			{
				removeAllFromParentView();
			}
			if (contentsOperable)
				makeThisAllGoAway(!broadcast);
		}
	}
	
	/**
	 * Sets the component state of a Location.
	 *
	 * @see twisted.reality.Thing.setComponent(boolean)
	 */
	
	public void setComponent(boolean yn)
	{
		if (comp==yn) return;
		super.setComponent(yn);
		if (isBroadcast() && (loc != null))
		{
			if (comp)
			{
				addAllToParentView();
			}
			else
			{
				removeAllFromParentView();
				/*
				 * This is somewhat of a hack for being too lazy to
				 * fix the client... it's not too bad, because it's
				 * consistent, but broadcast objects don't work
				 * aesthetically 100% correctly.  If they're nailed,
				 * they display their contents non-heirarchically, and
				 * if they're not, they display their contents as part
				 * of their own isHere message.  Ideally, the content
				 * should heirarchicalize the messages itself.
				 */
			}
		}
	}
	
	private boolean contentsVisible=true;
	/**
	 * Sets the visibility of the contents in this Location.
	 * Visibility in this context means whether they can be seen by a
	 * player looking at this Location -- therefore, a closed location
	 * would have invisible objects.  This is translated to
	 * closedContainer.setContentsVisible(false); in code.
	 */
	public void setContentsVisible(boolean inContentsVisible)
	{
		if (inContentsVisible!=contentsVisible)
		{
			if (!inContentsVisible)
				setBroadcast(false);
			contentsVisible=inContentsVisible;
			itemRefreshMyObservers();
		}
	}
	
	/**
	 * This returns whether or not the contents of this Location will
	 * be visible to a player looking at it.
	 */
	
	public boolean areContentsVisible()
	{
		return contentsVisible;
	}
	
	private boolean contentsOperable=true;
	
	/**
	 * Returns whether or not the contents of this object are
	 * operable.  Operable, in this context, is defined as whether or
	 * not a player trying to get an object from this Location to do
	 * something with it can do so.  A closed container's contents,
	 * for example, would be inoperable.
	 */
	
	public boolean areContentsOperable()
	{
		return contentsOperable;
	}

	/**
	 * Sets the operability of the contents of this Location.
	 * Operable, in this context, is defined as whether or not a
	 * player trying to get an object from this Location to do
	 * something with it can do so.  A closed container's contents,
	 * for example, would be inoperable.
	 */

	public void setContentsOperable(boolean inContentsOperable)
	{
		if (contentsOperable == inContentsOperable) return;
		/* this will remain poorly implemented until a future
		 * version. the idea is that there will be an exception thrown
		 * when you find an 'inoperable' object (such as something
		 * inside a transparent container) which contains a copy of a
		 * reference to the object, so that 'smart' verbs (like
		 * 'look') can operate inoperable objects.
		 */
		
		contentsOperable=inContentsOperable;
		
		if (broadcast)
		{
			makeThisAllGoAway(!contentsOperable);
		}
	}

	/**
	 * This either copies or removes our list of sub-synonyms from our
	 * parent.
	 */

	private void makeThisAllGoAway(boolean reallyAway)
	{
		Enumeration e;
		if ((loc==null) || 
			(inventory==null) ||
			((e = inventory.elements())==null))
			return;


		if (reallyAway)
			while(e.hasMoreElements())
				loc.removeSyns((Thing)e.nextElement());
		else
			while(e.hasMoreElements())
				loc.addSyns((Thing)e.nextElement());
	}
	
	/**
	 * Returns whether this location is broadcasting its contents to
	 * be visible in its container.
	 */
	
	public boolean isBroadcast()
	{
		return broadcast;
	}
	
	String content()
	{
		StringBuffer sbr = new StringBuffer(super.content());
		if(broadcast)
		{
			sbr.append("\n\tbroadcast");
		}
		if(!contentsVisible)
		{
			sbr.append("\n\topaque");
		}
		if(!contentsOperable)
		{
			sbr.append("\n\tshut");
		}
		return sbr.toString();
	}
	
	/**
	 * Broadcast an event to every object present in this location.
	 * @see twisted.reality.RealEvent
	 */
	
	public void broadcastEvent(RealEvent e)
	{
		/* EVERY object present */
		Enumeration f = things(true,true);
		while(f.hasMoreElements())
		{
			Thing t = (Thing) f.nextElement();
			t.handleEvent(e);
		}
	}
	
	/**
	 * Broadcast an event to every object in this room, a certain
	 * number of game-beats into the future. (One game-beat is 10*PI
	 * seconds.)
	 * 
	 * @param e the event to broadcast
	 * 
	 * @param a how long to wait.
	 */
	
	public void broadcastDelayedEvent(RealEvent e, int a)
	{
		Age.theUniverse().installDelayedEvent(e,a,this,true);
	}
	
	/**
	 * Removes a single synonym from the internal list of objects in
	 * this room.
	 *
	 * @param s The synonym to be removed
	 *
	 * @param x The Thing the synonym is for
	 */
	
	void removesingle(String s, Thing x)
	{
		// I'm not exactly clear on *why* syns is null sometimes when
		// this happens, but let's just pretend it is...
		if ( (s==null) || (x == null) || (syns == null) ) return;
		String o = s.toLowerCase();
		Object ot = syns.get(o);
		
		if(ot != null)
		{
			if(ot instanceof AmbiguityRecord)
			{
				AmbiguityRecord a = (AmbiguityRecord) ot;
				Thing t = a.lessAmbiguous(x);
				if (t!=null)
					syns.put(o,t);
			}
			else if (ot == x)
			{
				syns.remove(o);
				/* garbage collect unused tables */
				if ( syns.isEmpty() ) syns=null;
			}
		}
	}
	
	void removeSyns(Thing x)
	{
		Enumeration e = x.names();
		removesingle(x.NAME(),x);
		String s = x.name();
		if(!s.equals(x.NAME()) )removesingle(s,x);
		
		while(e.hasMoreElements())
		{
			Object o = e.nextElement();
			removesingle((String)o,x);
		}
		
	}
	
	void singlesyn(String s, Thing x)
	{
		String o = s.toLowerCase();
		if(syns.get(o)==null)
		{
			syns.put(o,x);
		}
		else
		{
			Object theo = syns.get(o);
			
			if(theo instanceof AmbiguityRecord)
			{
				AmbiguityRecord a = (AmbiguityRecord) theo;
				a.moreAmbiguous(x);
			}
			else if (theo instanceof Thing)
			{
				Thing t = (Thing) theo;
				syns.put(o,new AmbiguityRecord(t,x));
			}
		}
		
	}
	
	void addSyns(Thing x)
	{
		Enumeration e = x.names();
		singlesyn(x.NAME(),x);
		
		
		/* can't do this because of the "name" property.  Workaround:
		   please add a synonym for the *apparent* fqdn of your object
		   */
		
		/* if(!s.equals(x.NAME()) )singlesyn(s,x); */
		
		while(e.hasMoreElements())
		{
			Object o = e.nextElement();
			singlesyn((String)o,x);
		}
	}

	private void addToMyView(Thing x)
	{
		if(x.isComponent()) return;
		synchronized(myObservable)
		{
			Enumeration e = myObservable.elements(); if (e == null) return;
			while(e.hasMoreElements())
			{
				Player p = (Player) e.nextElement();
				p.notifyEntered(x);
			}
		}
	}
	
	private void addToParentView(Thing x)
	{
		if(loc!=null)
			loc.addToMyView(x);
	}
	
	private void removeFromMyView(Thing x)
	{
		synchronized(myObservable)
		{
			Enumeration e = myObservable.elements(); if (e == null) return;
			while(e.hasMoreElements())
			{
				Player p = (Player) e.nextElement();
				p.notifyLeft(x);
			}
		}
	}
	
	private void removeFromParentView(Thing x)
	{
		if(loc!=null)
			loc.removeFromMyView(x);
	}
	
	private void addAllToParentView()
	{
		if (loc == null) return;
		Enumeration e = things(); if (e == null) return;
		while(e.hasMoreElements())
		{
			Thing t = (Thing) e.nextElement();
			loc.addToMyView(t);
		}
	}
	
	private void removeAllFromParentView()
	{
		if (loc == null) return;
		Enumeration e = things(); if (e==null) return;
		while(e.hasMoreElements())
		{
			Thing t = (Thing) e.nextElement();
			loc.removeFromMyView(t);
		}
	}

	synchronized void toss(Thing x)
	{
		if(x==null) return;
		
		if((inventory!=null) && (inventory.get(x.NAME().toLowerCase())!=null))
		{
			inventory.remove(x.NAME().toLowerCase());
			removeSyns(x);
			if(contentsVisible)
			{
				removeFromMyView(x);
				if (loc != null)
				{
					if (broadcast)
					{
						//if (comp)
						removeFromParentView(x);
						// else
						// loc.updateNameFor(this);
						if (contentsOperable)
							loc.removeSyns(x);
					}
				}
			}

			/* garbage collect unused tables */
			if (inventory.isEmpty()) inventory=null;
		}
	}
	
	/**
	 * Returns the Location's type-name for outputting files. (In this
	 * case, Location)
	 */
	
	String typeName()
	{
		return "Location";
	}
	
	synchronized void updateNameFor(Thing x)
	{
		if ( (x != null) && (x.place()==this) && areContentsVisible() )
		{
			// This is a temporary hack.  The reasons for this are
			// described in NetClientUser.
			if(!x.isComponent())
			{
				addToMyView(x);
				
				if (broadcast
					&& loc!=null)
				{
					loc.addToMyView(x);
				}
			}
			else
			{
				removeFromMyView(x);
				
				if (broadcast
					&& loc!=null)
				{
					loc.removeFromMyView(x);
				}
			}
		}
	}
	
	synchronized void grab(Thing x)
	{
		if(inventory == null) inventory=dict();
		if(syns == null) syns=dict();
		
		if( inventory.get(x.NAME().toLowerCase()) != x )
		{
			inventory.put(x.NAME().toLowerCase(),x);
			addSyns(x);
		}
		if(contentsVisible)
		{
			addToMyView(x);
			if (loc != null && broadcast)
			{
				addToParentView(x);
				if (contentsOperable)
					loc.addSyns(x);
			}
		}
	}
	
	/**
	 * Returns the number of objects currently located in this location.
	 */
	public int thingCount()
	{
		if (inventory==null) return 0;
		else return inventory.size();
	}
	
	/**
	 * Returns an enumeration of every shown (i.e. non-component)
	 * object in this location, including Players.  If this location's
	 * contents are not visible, it returns an empty enumeration.
	 */
	
	public Enumeration things()
	{
		return things(true);
	}
	
	/**
	 * Returns an enumeration of every shown (i.e. non-component)
	 * object in this location, conditionally excluding Players.  If
	 * this location's contents are not visible, it returns an empty
	 * enumeration.
	 *	
	 * @param includePlayers If this is true, Things of class
	 * twisted.reality.Player will be included in the result.  If
	 * not, they won't.
	 */
	
	public Enumeration things(boolean includePlayers)
	{
		return things(includePlayers,false);
	}
	
	/**
	 * Returns an enumeration of elements in this location, optionally
	 * including players and/or hidden objects.
	 */
	
	public Enumeration things(boolean includePlayers,
							  boolean showHidden)
	{
		if (!contentsVisible && !showHidden)
		{
			return twisted.util.EmptyEnumeration.EMPTY;
		}
		Enumeration retE = new StuffEnumeration(this);
		if (includePlayers)
			return retE;
		else
		{
			try
			{
				return new ReverseClassEnumeration(retE,Class.forName("twisted.reality.Player"));
			}
			catch (ClassNotFoundException e)
			{
				Age.log("Wow, there's no such thing as a Player.");
				Age.log("Error weighting: Extremely Bad Thing");
				return null;
			}
		}
	}
	
	private class StuffEnumeration implements java.util.Enumeration
	{
		Enumeration myE;
		Enumeration myE2;
		
		StuffEnumeration (Location l)
		{
			if (l.inventory != null)
			{
				myE = l.inventory.elements();
			}
		}
		
		public boolean hasMoreElements()
		{
			if (myE == null) return false;
			if (cached==null)
			{
				if (myE2 == null)
				{
					if (myE.hasMoreElements())
					{
						cached=(Thing)myE.nextElement();
						if ((cached instanceof Location) && ((Location)cached).broadcast)
						{
							myE2=((Location)cached).things();
						}
						return true;
					}
					else
						return false;
				}
				else
				{
					if (myE2.hasMoreElements())
					{
						cached = (Thing)myE2.nextElement();
						return true;
					}
					else
					{
						myE2=null;
						return hasMoreElements();
					}
				}
			}
			else
				return true;
		}

		public Object nextElement()
		{
			if(hasMoreElements())
			{
				Thing c2=cached;
				cached=null;
				return c2;
			}
			else
			{
				return null;
			}
		}
		
		Thing cached;
	}
	
	/**
	 * Looks for a thing with a given name in the current room.
	 * 
	 * @param s The name of the thing to look for
	 */
	
	public Thing findThing(String s, Thing looker) throws AmbiguousException
	{
		if((syns == null) || !contentsOperable) return null;

		Object o = syns.get( s.toLowerCase() );
		
		if (o == null) return null;
		
		if(o instanceof Thing)
		{
			return (Thing) o;
		}
		
		AmbiguityRecord a = (AmbiguityRecord) o;
		
		throw new AmbiguousException(a.elements(),s,looker);
	}

	Dictionary syns;
	Dictionary inventory;
	
	/**
	 * Returns a String built out of the Object[] o if all the
	 * elements of o are static.  If there are any dynamic elements in
	 * o, it returns null.
	 */
	String optimizeStringArray(Object[] s)
	{
		boolean onlyStrings = true;
		for (int i = 0; i<s.length; i++)
		{
			if (s[i] instanceof Thing || s[i] instanceof Perceptible)
				onlyStrings = false;
		}

		if(onlyStrings)
		{
			StringBuffer tapt=new StringBuffer();
			for (int i = 0; i<s.length; i++)
			{
				tapt.append(s[i]);
			}
			return tapt.toString();
		}
		else
			return null;
	}
	/**
	 * Sends a message to everyone in the room.  Note that an Object[]
	 * is used instead of a string so that names and other dynamic
	 * elements in the string will get evaluated for each Player.
	 *
	 * Example usage: <pre>
	 
	 Object[] subj =  {"You wave to ",
	                   Name.of(d.directObject())," and ",
	                   Pronoun.of(d.directObject()), " nods."}};
					   
	 Object[] targ =  {Name.Of(d.subject()),
	                   " waves to you, and you nod."};
					   
	 Object[] other = {Name.Of(d.subject()),
	                   " waves to ", Name.of(d.directObject()),
	                   ", and ",
	                   Pronoun.of(d.directObject()), " nods."};
					   
	 d.place().tellAll(d.subject(),
	                   (Player)d.directObject(),
	                   subj, targ, other);
	 * </pre>
	 * 
	 * In this example, when bob executes "wave to jethro", the effect
	 * is as follows:<ul> <li>BOB hears: "You wave to Jethro, and he
	 * nods."<li>JETHRO hears: "Bob waves to you, and you
	 * nod."<li>EVERYONE ELSE hears: "Bob waves to Jethro, and he
	 * nods."</ul>
	 * 
	 * This example would be used e.g. in a Wave verb.
	 *
	 * @param subject the Player sending the message.
	 * 
	 * @param target the Player the message is directed to.
	 * 
	 * @param toSubject this message will be sent to the Player subject.
	 * 
	 * @param toTarget this message will be sent to the Player target.
	 * 
	 * @param toOther this message will be sent to everyone else.
	 * 
	 * @see twisted.reality.Name
	 * 
	 * @see twisted.reality.Pronoun
	 * 
	 * @see twisted.reality.Perceptible
	 */
	public void tellAll(Thing subject,
						Thing target,
						Object[] toSubject,
						Object[] toTarget,
						Object[] toOther)
	{
		String toOtherString = null;
		if(toOther != null)
			toOtherString = optimizeStringArray(toOther);
		
		Enumeration pl = players(true);
		while (pl.hasMoreElements())
		{
			Player pr = (Player)pl.nextElement();
			if (pr == subject)
			{
				if(toSubject != null)
					pr.hears(toSubject);
			}
			else if (pr == target)
			{
				if(toTarget != null)
					pr.hears(toTarget);
			}
			else
			{
				if(toOtherString != null)
					pr.hears(toOtherString);
				else if(toOther != null)
					pr.hears(toOther);
			}
		}
	}
	
	/**
	 * Sends a message to everyone in the room.  Note that an Object[]
	 * is used instead of a string so that names and other dynamic
	 * elements in the string will get evaluated for each Player.
	 *
	 * @param subject the Player sending the message.
	 * 
	 * @param toSubject this message will be sent to the Player subject.
	 * 
	 * @param toOther this message will be sent to everyone else.
	 */
	public void tellAll(Thing subject,
						Object[] toSubject,
						Object[] toOther)
	{
		tellAll(subject,null,toSubject,null,toOther);
	}
	
	/**
	 * Sends a message to everyone in the room.  This form of tellAll
	 * should be used when there isn't a specific Player who is the
	 * source of the message. (an example would be Gate disappearing)
	 * Note that an Object[] is used instead of a string so that names
	 * and other dynamic elements in the string will get evaluated for
	 * each Player.
	 *
	 * @param toAll this message will be sent to the everyone.
	 */
	
	public void tellAll(Object[] toTell)
	{
		if(toTell == null) return;
		Enumeration pl = players(true);
		
		String toTellString = optimizeStringArray(toTell);
		
		if(toTellString == null)
		{
			while(pl.hasMoreElements())
			{
				((Player)pl.nextElement()).hears(toTell);
			}
		}
		else
		{
			while(pl.hasMoreElements())
			{
				((Player)pl.nextElement()).hears(toTellString);
			}
		}
	}

	/**
	 * This function sends the string s to everyone in this location
	 * but Player p.
	 * 
	 * This function can not be used to refer to objects that actually
	 * exist in the world, as it does not deal with perspectives
	 * properly. Location.tellAll should be used instead.
	 */
	
	public void tellEverybody(String s)
	{
		Enumeration e = players(true);
		Player th;
		if(e!=null)
		{
			while(e.hasMoreElements())
			{
				th=(Player) e.nextElement();
				th.hears(s);
			}
		}
	}

	/**
	 * This function sends the string s to everyone in this location
	 * but Player p.  This can not be used to refer to objects
	 * actually present in the game, as it does not deal with
	 * perspectives properly. Location.tellAll should be used instead.
	 */ 
	
	public void tellEverybodyBut(Player p,String s)
	{
		Enumeration e = players(true);
		Player th;
		if(e!=null)
		{
			while(e.hasMoreElements())
			{
				th=(Player) e.nextElement();
				if(th!=p) th.hears(s);
			}
		}
	}
	
	/**
	 * This function sends the string s to everyone in this location
	 * but Player p and Player pt.
	 * 
	 * This function can not be used to refer to objects actually
	 * present in the world, as it does not deal with perspectives
	 * properly. Location.tellAll should be used instead.
	 */
	
	public void tellEverybodyBut(Player p, Player pt, String s)
	{
		Enumeration e = players(true);
		Player th;
		if(e!=null)
		{
			while(e.hasMoreElements())
			{
				th=(Player) e.nextElement();
				if(th!=p && th!=pt) th.hears(s);
			}
		}
	}
	
	/**
	 * Returns an Enumeration of all the players in the room.
	 */
	
	public Enumeration players()
	{
		return players(false);
	}
	
	public Enumeration players(boolean showHidden)
	{
		return new ClassBasedEnumeration(things(true,showHidden),Player.class);
	}
}
