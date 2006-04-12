package twisted.reality.plugin.door;

import twisted.reality.*;

/**
 * This is a silly sarcastic verb for swinging doors in the demo... It
 * doesn't really do anything useful, since swinging doors don't
 * really impede motion through the exit.
 * 
 * @author Tenth */

public class OpenCloseSwingingDoor extends Verb
{
	public OpenCloseSwingingDoor()
	{
		super ("open");
		alias ("close");
		alias ("push");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing t = d.directObject();
		Player p = d.subject();
		Room r = (Room) d.place();
		String verb = d.verbString();
		Portal way = r.getPortalByThing(t);
		Room there = way.sRoom(); //The room the exit leads to

		if (verb.equals("close"))
		{
			Object[] pDumb = 
			{"The door is already closed."};
			Object[] oDumb = 
			{p," stares at the door."};
			r.tellAll(p, pDumb, oDumb);
		}
		else
		{
			Object[] pHears = 
			{"You push open ",t,", and after a moment it swings shut again."};
			Object[] oHears = 
			{p," pushes ",t," open for a moment, and watches as it swing shut again."};
			r.tellAll(p, pHears, oHears);
			Object[] oOHears =
			{p," pushes open ",t," and disappears from view as it swings shut again."};
			there.tellAll(oOHears);
		}

		return true;
	}
}
