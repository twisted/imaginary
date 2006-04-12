package divunal.tenth;

import twisted.reality.*;
import divunal.tenth.SteamEngineEvent;

public class LibraryPush extends Verb
{
	public LibraryPush()
	{
		super("push");
		alias("press");
	}
	
	public static final int RED=0;
	public static final int YELLOW=1;
	public static final int GREEN=2;
	
	public static void pushRed(Thing door, Room room)
	{
		room.tellEverybody("There is a loud hissing sound, and a jet of steam shoots out rather abruptly from under each shelf for a few seconds, before trailing off and falling silent.");
	}
	
	public static void pushGreen(Thing door, Room room)
	{
		Portal way = room.getPortalByThing(door);
		
		if(!door.getBool("obstructed"))
		{
			room.tellEverybody("You hear a faint hissing sound.");
		}
		else if(door.getBool("yellow pushed"))
		{
			room.tellEverybody("There is a soft hissing sound as the shelves slide to the right, recentering them.");
			door.putBool("yellow pushed", false);
		}
		else
		{
			room.tellEverybody("There is a soft hissing sound as the shelves slide to the right, making the leftmost two shelves more easily accessible and revealing a small wooden framed doorway in the north wall.");				
			door.putBool("obstructed",false);
			if(way != null)
			{
				way.setObvious(true);
				Portal yaw = way.backtrack();
				yaw.setObvious(true);
			}
		
			room.putDescriptor("bookshelf door open", "There is a small doorway to the north between two of the bookshelves.");
			Room other = room.getPortalByThing(door).sRoom();
			other.tellEverybody("Steam hisses out of the pistons attached to the door, and it swings open.");
			other.putDescriptor("bookshelf door","The door to the south stands open.");
			door.handleDelayedEvent(new RealEvent("shelf close",null,null),1);		
		}
	}
	
	public static void pushYellow(Thing door, Room room)
	{
		if(door.getBool("yellow pushed"))
		{
			room.tellEverybody("You hear a faint hissing sound.");
		}
		else if(door.getBool("obstructed"))
		{
			
			room.tellEverybody("There is a soft hissing sound as the shelves slide to the left, making the rightmost two shelves more easily accesible.");
			door.putBool("yellow pushed",true);
		}
		else
		{
			door.handleEvent(new RealEvent("shelf close",null,null));
		}
	}
	
	
	public void pushButton(Thing door, Room room, int colorstat, int steampressure, Thing steamsource)
	{
		if (steampressure > 50)
		{
			switch(colorstat)
			{
			case RED:
				pushRed(door,room);
				steampressure = 0;
				break;
				
			case GREEN:
				pushGreen(door,room);
				steampressure -= 100;
				break;
			case YELLOW:
				pushYellow(door,room);
				steampressure -= 100;
				break;
			}

			SteamEngineEvent.updateSteamGauge(steamsource, steampressure);
		}
		else
		{
			String str = "There is a hollow metallic clunking noise from somewhere under the floor beneath the bookshelves.";
			room.tellEverybody(str);
			room.getPortalByThing(door).sRoom().tellEverybody(str);
		}
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		String s = d.directString();
		Room room = (Room) d.place();
		Thing door = room.getThing("bookshelf door");
		Thing steamsource = door.getThing("steam source");
		int steampressure = steamsource.getInt("steam pressure");
		int colorstat=-1;
		String buttoncolor="huh?";

		if (s.startsWith("red"))
		{
			colorstat=RED;
			buttoncolor="red";
		}
		else if (s.startsWith("yellow"))
		{
			colorstat=YELLOW;
			buttoncolor="yellow";
		}
		else if (s.startsWith("green"))
		{
			colorstat=GREEN;
			buttoncolor="green";
		}
		if (colorstat != -1)
		{
			Object[] sptb = {p, " pushes the " +buttoncolor+ " button."};
			Object[] yptb = {"You push the "+buttoncolor+" button."};
			room.tellAll(p,yptb,sptb);
		}
		else
		{
			p.hears("What button do you want to push?");
		}
		
		pushButton(door,room,colorstat,steampressure, steamsource);
		
		return true;
	}
}
