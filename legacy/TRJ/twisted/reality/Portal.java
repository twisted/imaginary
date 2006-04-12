package twisted.reality;
import java.util.Enumeration;
/**
 * This represents a one-way exit between two rooms. Two-way exits are
 * two portals that complement each other, such as those created by
 * Portal.between().
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Portal extends Nameable
{
	/**
	 * Creates a new portal from one room, to another, with a
	 * specified name for a direction.
	 *
	 * @param x The room in which the exit resides.
	 * 
	 * @param y The room to which the exit exits.
	 * 
	 * @param a The string that names the exit.
	 */
	
	public Portal(Room x,Room y,String a)
	{
		super(a);
		myRoomRef=y.ref;
		ofOrigin=x;
		x.addPortal(this);
	}
	
	/**
	 * Propels any object through the exit, if it is open.	Has the
	 * player listen to the exit message, if there is a message to
	 * be listened to (and the object is a player).
	 *	
	 * @param x The player to be moved.
	 */
	
	public void propels(Thing x)
	{
		if( sRoom()==null )
		{
			if(x instanceof Player)
			{
				((Player)x).hears("That exit suddenly shimmers out of existence.");
			}
			ofOrigin.removePortal(name());
			return;
		}
		Object[] exitmsg={"You go ", name(), "."};
		if(sThing() != null)
		{
			if(sThing().getBool("obstructed"))
			/* XXX DOCUMENT THIS ^^^^^^^^^^ */
			{
				if(x instanceof Player)
				{
					if(sThing().getString("obstructed message") != null)
						((Player)x).hears(sThing().getString("obstructed message"));
					else
						((Player)x).hears("The way appears to be blocked.");
				}
				return;
			}
			else
			{
				if(sThing().getString("exit message")!=null)
				{
					Object[] blert={sThing().getString("exit message")};
					exitmsg=blert;
				}
			}
		}

		Object[] entermsg=new Object[2];
		Portal b = backtrack();
		
		entermsg[0]=x;	
	
		if (b != null)
		{
			String bt = Age.intern(b.NAME());
			if (bt == "up")
			{
				entermsg[1]= " enters from above.";
			}
			else if (bt == "down")
			{
				entermsg[1]= " enters from below.";
			}
			else
			{
				entermsg[1]= " enters from the " + bt + ".";
			}
		}
		else
		{
			entermsg[1] = " enters.";
		}
		Object[] tmpext={x," goes ",NAME(),"."};
		x.moveTo(sRoom(),tmpext,entermsg);
		if (x instanceof Player) ((Player)x).hears(exitmsg);
	}
	
	/**
	 * A simple macro function to hook two rooms together. Makes two portals,
	 * one from a to b, and one from b to a.
	 * 
	 * @param a The first room
	 * 
	 * @param b The second room
	 * 
	 * @param c The direction from the first room to the second.
	 * (The direction from the second to the first is the reverse of
	 * that.)
	 * 
	 * @see reverse 
	 */
	
	public static void between(Room a, Room b, String c)
	{
		new Portal(a,b,c);
		new Portal(b,a,reverse(c));
	}
	
	/**
	 * A simple macro function to hook two rooms together. Makes two portals,
	 * one from a to b, and one from b to a. Both are arbitrated with Thing d.
	 * 
	 * @param a The first room
	 * 
	 * @param b The second room
	 * 
	 * @param c The direction from the first room to the second.
	 * (The direction from the second to the first is the reverse of
	 * that.)
	 * 
	 * @param d The 'door' that arbitrates the exit.
	 * @see reverse 
	 * @see setThing(Thing)
	 */
	public static void between(Room a, Room b, String c, Thing d)
	{
		Portal p = new Portal(a,b,c);
		Portal q = new Portal(b,a,reverse(c));
		d.place(a);
		p.setThing(d);
		q.setThing(d);
	}

	/**
	 * Finds the portal that is the opposite of this one.
	 * If this portal goes from room A to room B, this function will
	 * return the (first) portal that goes from room B to room A.
	 */
	public Portal backtrack()
	{
		Room r = sRoom();
		Enumeration e = r.allPortals();
		
		if (e != null)
		{
			while (e.hasMoreElements())
			{
				Portal p = (Portal) e.nextElement();
				if (p.sRoom() == ofOrigin)
				{
					return p;
				}
			}
		}
		return null;
	}
	
	/**
	 * Takes a string which represents a direction and returns its
	 * reverse.
	 *
	 * @param x the String to reverse
	 * 
	 * @see between
	 * 
	 * @return "south" for "north", "up" for "down", etc.
	 */
	
	public static final String reverse(String x)
	{
		String s = null;
		
		String y = x.toLowerCase().intern();
		
		if(y=="north") return "south";
		if(y=="northeast") return "southwest";
		if(y=="east") return "west";
		if(y=="southeast") return "northwest";
		if(y=="south") return "north";
		if(y=="southwest") return "northeast";
		if(y=="west") return "east";
		if(y=="northwest") return "southeast";
		if(y=="up") return "down";
		if(y=="down") return "up";
		
		return "back";
	}
	
	Room ofOrigin;
	
	/**
	 * Returns the room the exit points to.
	 */
	
	public final Room sRoom()
	{
		if(myRoomRef != null)
		{
			return (Room) myRoomRef.sThing();
		}
		else
		{
			Age.log("twisted.reality.Portal: bug.  myRoomRef is null. this should never happen.");
			return null;
		}
	}
	
	/**
	 * Returns the Thing that arbitrates this exit.  This thing
	 * is usually something like a door. If its property
	 * 'obstructed' is true, the exit is impassible. This thing
	 * exists in both the room that the portal goes from as
	 * well as the room the portal goes to, via some wicked
	 * hackery that you'd rather not know about.
	 */
	public final void setThing(Thing t)
	{
		if (sThing() != null)
		{
			if (sThing().place() != ofOrigin)
			{
				ofOrigin.toss(t);
			}
		}
		if(t!=null)
		{
			myThingRef=t.ref;
			t.setComponent(true);
			if(t.place() != ofOrigin)
			{
				ofOrigin.grab(t);
				// this allows my door to be in two places at once
				// I wonder how much havoc this will wreak?
				// 
				// answer: ALL KINDS.  This is an awful, awful hack,
				// and reveals one of the few things that TR still
				// can't do right.  We need to have some mechanism for
				// doing multiple locations.
			}
		}
		else
		{
			myThingRef=null;
		}
	}
	
	/**
	 * Returns the Thing that arbitrates this exit. 
	 */
	public final Thing sThing()
	{
		if (myThingRef != null) return myThingRef.sThing();
		return null;
	}
	
	/**
	 * Sets whether this exit is obvious or not. If it is obvious,
	 * it will be listed in the Exits list.
	 */
	public final void setObvious(boolean b)
	{
		if (b!=obvious)
		{
			obvious=b;
			//if(ofOrigin != null) ofOrigin.tellObservers(new RealEvent("describe",ofOrigin.describe(),ofOrigin));
			if(ofOrigin != null)
				synchronized(ofOrigin.myObservable)
				{
					Enumeration e = ofOrigin.myObservable.elements();
					while(e.hasMoreElements())
					{
						Player p = (Player) e.nextElement();
						p.focusRefresh();
					}
				}
		}
	}
	
	/**
	 * Returns if this exit is obvious or not. If it is obvious,
	 * it will be listed in the Exits list.
	 */
	public final boolean isObvious()
	{
		return obvious;
	}

	boolean obvious=true;

	/**
	 * The Room the object leads to if it is open.
	 */
	
	ThingIdentifier myRoomRef;

	/**
	 * The thing that this exit asks permission of.
	 */
	
	ThingIdentifier myThingRef;
}
