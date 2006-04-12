package inheritance.clock;

import twisted.reality.*;

public class ClockStart extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		thisThing.putLong("init time", System.currentTimeMillis());
	}
}
