package twisted.reality;

import java.util.Dictionary;
import java.util.Hashtable;
import java.util.Enumeration;
import twisted.util.ReverseClassEnumeration;
import twisted.util.ClassBasedEnumeration;
import twisted.util.StringLegalizer;
import twisted.util.LinkedList;

/**
 * This is a location from which there may be many exits.  Typically,
 * it is the location where most actions take place.  Room is also a
 * subclass of Thing, so it may be treated as a Thing as well.
 * Properties may also be stored on Rooms in the same manner.
 * 
 * @version 1.0.0, 1 Jul 1999
 * @author Glyph Lefkowitz
 */

public class Room extends Location
{
	/**
	 * Create a room with a name and a description.
	 *
	 * @param a The name of the new room
	 * 
	 * @param b The description of the new room.
	 */ 
	
	public Room(String a, String b)
	{
		this(null, a, b);
	}
	
	/**
	 * Create a new, unnamed, undescribed Room.  This will not be
	 * stored as part of the map unless it is named.
	 */
	
	Room()
	{
		super();
	}
	
	String typeName()
	{
		return "Room";
	}
	
	// This is also fairly kludgy.  Gaah!
	/**
	 * Retuns the portal that is arbitrated by Thing t.
	 */
	public Portal getPortalByThing(Thing t)
	{
		if(portals == null) return null;
		Enumeration e = portals.elements();
		while(e.hasMoreElements())
		{
			Portal p = (Portal)e.nextElement();
			if(p.sThing()==t)
			{
				return p;
			}
		}
		return null;
	}
	
	/**
	 * Returns the room to a given direction, or null, if the exit
	 * leading there is nonexistant.
	 *
	 * @param direction The name of the direction the room's in.
	 */
	
	public Room toThe(String direction)
	{
		Portal p = getPortal(direction);
		if(p!=null) return p.sRoom();
		return null;
	}
	
	String content()
	{
		StringBuffer r = new StringBuffer(super.content());
		
		if(portals != null)
		{
			Enumeration e = portals.elements();
			
			while(e.hasMoreElements())
			{
				
				// format of these strings:
				// exit "north" to "A Room" [with "A Door"]
				
				Portal p = (Portal) e.nextElement();
				
				if ( p.sRoom() != null)
				{
					r.append("\n\texit \"").append(StringLegalizer.legalize( p.name())).append("\" ").append((p.isObvious()?"to":"notTo")).append(" \"").append(StringLegalizer.legalize(p.sRoom().NAME())).append("\"");
					if (p.sThing() != null)
					{
						r.append(" with \"").append(StringLegalizer.legalize(p.sThing().NAME())).append("\"");
					}
				}
			}
			if (!portalsVisible)
			{
				r.append("\n\tclaustrophobic");
			}
		}
		
		return r.toString();
	}
	
	/**
	 * Create a room with the given Location, name, and description.
	 * This creates a fully-qualified Room and will be stored in the
	 * map.
	 * 
	 * @param a The place the new Room will be stored
	 * 
	 * @param b The name of the new room
	 * 
	 * @param c The initial description of the new room
	 */
	
	public Room(Location a, String b, String c)
	{
		super(a,b,c);
	}
	
	/**
	 * Tries to move the room - and always fails.  Rooms do not
	 * typically move.
	 */
	
	public boolean moveTo(Location l, String s)
	{
		return false;
	}
	
	/**
	 * Adds the given portal to this room.
	 * 
	 * @param x The portal to add
	 */
	
	public void addPortal(Portal x)
	{
		if(portals == null) portals=dict();
		{
			portals.put(x.NAME().toLowerCase(),x);
			// if(myObservable!=null) tellObservers(new RealEvent("describe",null,this));
			focusRefreshMyObservers();
		}
	}
	
	/**
	 * Removes the given portal from the room.
	 * 
	 * @param x The portal to remove
	 */
	
	public void removePortal(String x)
	{
		if(portals!=null)
		{
			portals.remove(x.toLowerCase());
			/* garbage collect empty tables */
			if (portals.isEmpty())
				portals=null;
			focusRefreshMyObservers();
		}
	}
	
	/**
	 * Returns the portal in the direction specified, or 
	 * 
	 * @param portalName The name of the portal to fetch.
	 */
	
	public Portal getPortal(String portalName)
	{
		return ((portals == null) ? null : (Portal) portals.get(portalName.toLowerCase()));
	}
	
	/**
	 * Returns an enumeration of all the portals in this room.
	 */
	public Enumeration allPortals()
	{
		if (portalsVisible)
		{
			return (portals==null) ? twisted.util.EmptyEnumeration.EMPTY : portals.elements();
		}
		return twisted.util.EmptyEnumeration.EMPTY;
	}
	
	boolean portalsVisible=true;
	
	/**
	 * Returns if the portals in this room are hidden or not.
	 */
	public boolean arePortalsVisible()
	{
		return portalsVisible;
	}
	
	/**
	 * Sets the portals in this room to be hidden or not hidden.
	 */
	public void setPortalsVisible(boolean inPV)
	{
		if (inPV != portalsVisible)
		{
			portalsVisible=inPV;
			exitsRefreshMyObservers();
		}
	}
	
	/**
	 * Refreshes the exits in the client.
	 */
	public void exitsRefreshMyObservers()
	{
		/* right now, an exits change will always include a
		 * descriptive change.  This (lack of) code isn't correct, but
		 * I guess it should stay this way until we have some kind of
		 * transaction logic (shudder) in TR.
		 */
		
		/*focusRefreshMyObservers();*/
	}
	
	Dictionary portals;
}
