package inheritance.mummy;

import twisted.reality.*;

public class MummyDistracted extends RealEventHandler
{
	public void gotEvent (RealEvent re, Thing thisThing)
	{
		thisThing.removeProp("target");
		thisThing.removeProp("direction");

		/* debugging */
		thisThing.place().tellEverybody("The mummy was distracted by "+re.origin());
	}
}
