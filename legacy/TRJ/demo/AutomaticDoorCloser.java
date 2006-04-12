package demo;

import twisted.reality.*;

public class AutomaticDoorCloser extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing door)
	{			
		Room here = (Room) door.place();
		Portal p = here.getPortalByThing(door);
		if (p==null) return;
	    Room there = p.sRoom();
		String s = door.getString("close message");
		String closedDescription = door.getString("closedDescription");

		Object[] closing = {s};

		here.tellAll(closing);
		there.tellAll(closing);
		door.describe(closedDescription);
		twisted.reality.plugin.door.Door.close(door, false);
	}
}
