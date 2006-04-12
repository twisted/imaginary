package divunal.tenth;

import twisted.reality.*;

public class AtticCloseHandler extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		if(!thisThing.getBool("obstructed"))
		{
			thisThing.putBool("obstructed",true);
			Room r =  ((Room)thisThing.place());
			Portal way = r.getPortalByThing(thisThing);
			
			way.setObvious(false);
			r.tellEverybody("There is a faint hissing sound, and the wooden ladder retracts, folding back up behind a panel in the ceiling.");
			r.putDescriptor("attic door state","A small wooden ring is hanging from the center of the ceiling by a piece of string.");
		}
	}
}
