/* This is a utility class to modularize doing stuff with doors, e.g.
 * opening and closing.
 *
 * Author: Michael Dartt, jedin@divunal.com
 */

package twisted.reality.plugin.door;

import twisted.reality.*;

public final class Door
{

	/**
	 * Opens the given door.  
	 * In doing so, it changes the descriptions of the rooms the door is connected to, according to the following strings:
	 * <pre>
	 *     openDesc - description string added *to room where door is located*; what the players can see through the doorway
	 *     closeDesc - desc. string removed *from room where door is located*; what players see when door's closed
	 *     thereOpenDesc - desc. string added to connecting room
	 *     thereCloseDesc - desc. string removed from connecting room
	 * </pre>
	 * These are optional, but highly desireable for adding to the world's realism and richness
	 * Note that checks for stuff like whether the door is locked, etc. should be done in other verbs
	 * @param door - the Thing to be opened
	 * @param opener - the Player trying to open
	 *
	 */
	
	public static void open (Thing door, Player opener, Location place)
	{
		open(door, false);

		Object[] yotd={"You open ", door, "."};
		Object[] sotd={opener," opens ", door, "."};
		place.tellAll(opener,yotd,sotd);
		Object[] msg={Name.Of(door), " opens."};
		((Room)place).getPortalByThing(door).sRoom().tellAll(msg);
	}

	public static void open (Thing door)
	{
		open(door, true);
	}
	
	/**
	 * Opens the door, just as the above verb does.
	 * This form should be used when something besides a player is opening the door, e.g.
	 * someone flips a switch that opens the door, the door opens on its own, etc.
	 * 
	 * @param door - the Thing opening
	 * @param print - whether or not people should be informed that the door closed.  If this is false, some other function will have to handle telling people about it.
	 *
	 */

	public static void open (Thing door, boolean print)
	{
		Room here = (Room) door.place();
		Portal way = here.getPortalByThing(door);
		
		if (way != null)
		{
			Portal yaw = way.backtrack();
			Object[] msg = {Name.Of(door), " opens."};

			door.putBool("obstructed",false);
			
			//Update the description of the room in which the door's located
			//Note that here is where the door is, not (necessarily) where the player is
			here.removeDescriptor(door.NAME() + " closeDesc");
			String od = door.getString("openDesc");
			if (od != null)
			{
				here.putDescriptor(door.NAME() + " openDesc", od);
			}
			if (print)
			{
				here.tellAll(msg);
			}
			way.setObvious(true);
			
			if (yaw != null)
			{
				Room there = way.sRoom(); //The room the exit leads to
				
				//Update the description of the room the door leads to
				there.removeDescriptor(door.NAME() + " closeDesc");
				String tod = door.getString("thereOpenDesc");
				if (tod != null)
				{
					there.putDescriptor(door.NAME() + " openDesc", tod);
				}
				if (print)
				{
					there.tellAll(msg);
				}
				yaw.setObvious(true);
			}
		}
	}

	/**
	 * Closes the given door.  
	 * In doing so, it changes the descriptions of the rooms the door is connected to, according to the following strings:
	 * <pre>
	 *     openDesc - description string removed *from room where door is located*; what the players can see through the doorway
	 *     closeDesc - desc. string added *to room where door is located*; what players see when door's closed
	 *     thereOpenDesc - desc. string removed from connecting room
	 *     thereCloseDesc - desc. string added to connecting room
	 * </pre>
	 * These are optional, but highly desireable for adding to the world's realism and richness
	 * @param door - the Thing to be closed
	 * @param closer - the Player trying to close the door
	 */
	
	public static void close (Thing door, Player closer, Location place)
	{
		close(door, false);

		Object[] yotd={"You close ", door, "."};
		Object[] sotd={closer," closes ", door, "."};
		place.tellAll(closer,yotd,sotd);

		Object[] msg={Name.Of(door), " closes."};
		((Room)place).getPortalByThing(door).sRoom().tellAll(msg);
	}


	public static void close (Thing door)
	{
		close(door, true);
	}


	/**
	 * Closes the door, just as the above verb does.
	 * This form should be used when something besides a player is closing the door, e.g.
	 * someone flips a switch that closes the door, the door closes on its own, etc.
	 * 
	 * @param door - the Thing opening
	 * @param print - whether or not people should be informed that the door closed.  If this is false, some other function will have to handle telling people about it.
	 *
	 */

	public static void close (Thing door, boolean print)
	{	
		Room here = (Room) door.place();
		Portal way = here.getPortalByThing(door);
		
		if (way != null)
		{
			Portal yaw = way.backtrack();
			Object[] msg = {Name.Of(door), " closes."};

			door.putBool("obstructed",true);
			
			//Update the description of the room in which the door's located
			//Note that here is where the door is, not (necessarily) where the player is
			here.removeDescriptor(door.NAME() + " openDesc");
			String cd = door.getString("closeDesc");
			if (cd != null)
			{
				here.putDescriptor(door.NAME() + " closeDesc", cd);
			}
			if (print)
			{
				here.tellAll(msg);
			}
			way.setObvious(false);
			
			if (yaw != null)
			{
				Room there = way.sRoom(); //The room the exit leads to
				
				//Update the description of the room the door leads to
				there.removeDescriptor(door.NAME() + " openDesc");
				String tcd = door.getString("thereCloseDesc");
				if (tcd != null)
				{
					there.putDescriptor(door.NAME() + " closeDesc", tcd);
				}
				if (print)
				{
					there.tellAll(msg);
				}
				yaw.setObvious(false);
			}
		}
	
	}

}
