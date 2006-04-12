package demo;

import twisted.reality.*;

public class WaterOff extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		FountainPush.fountainOff(thisThing);
	}
}
