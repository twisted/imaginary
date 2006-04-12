package demo;

import twisted.reality.*;

// This is a generic Open/Close verb for
// containers.

public class AutomaticDoor extends Verb
{
	public AutomaticDoor()
	{
		super ("open");
		alias ("close");
		alias ("touch");
		alias ("unlock");
		alias ("lock");
		alias ("go");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing door = d.directObject();
		Player p = d.subject();
		Room here = (Room) d.place();
		String v = d.verbString();
		String openDescription = door.getString("openDescription");
		Portal port = here.getPortalByThing(door);
		String dir = port.name();

		if (door.getBool("obstructed") == true)
		{
			Object[] oSee = {p," begins to walk towards the doors, and they slide open as ",Pronoun.of(p)," approaches."};
			Object[] pSees = {"The doors slide open by themselves before you can get close enough to touch them."};
			Object[] pGoes = {"The doors slide open for you as you approach."};
			Object[] oGoes = {p, " walks through the doors to the south, which open as ",Pronoun.of(p)," approaches."};

			twisted.reality.plugin.door.Door.open(door, false);
			door.describe(openDescription);
			door.handleDelayedEvent(new RealEvent("door close",null,null),1);

			if (v.equals("go"))
			{
				if (d.directString().equals(dir))
				{
					here.tellAll(p, pGoes, oGoes);
					return false;
				}
				else
				{
					return false;
				}
			}
			else
			{
				here.tellAll(p, pSees, oSee);
			}
		}
		else
		{
			if (v.equals("go"))
			{
					return false;
			}
			else if (v.equals("open"))
			{
				p.hears("The doors are already open...");
			}
			else
			{
				p.hears("The doors are completely retracted into the walls, making that rather difficult.");
			}
			Object[] oDumb = {p, " stares at the doors for a moment."};
			here.tellAll(p, null, oDumb);
		}
		return true;
	}
}


/*
If Closed:

Everything will attempt to open, giving some kind of message to the
player, and a generic "As p approaches the door, it opens" to the
room.

If Open:

Attempts to move (go south, south, s) succeed. Attempts to do anything
else fail for various reasons, and player "stares at the door"
*/
