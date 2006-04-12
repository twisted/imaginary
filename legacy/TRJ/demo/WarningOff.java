package demo;

import twisted.reality.*;

public class WarningOff extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing place)
	{
		Location room = (Location) place;
		room.removeDescriptor("alert");
		room.tellEverybody("The warning lights retract into the ceiling compartments from whence they came, and the room suddenly falls silent.");
		room.removeProp("alert on");
	}
}
