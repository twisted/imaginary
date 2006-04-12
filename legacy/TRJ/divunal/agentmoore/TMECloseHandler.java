package divunal.agentmoore;

import twisted.reality.*;

public class TMECloseHandler extends RealEventHandler
{
    public void gotEvent(RealEvent e, Thing thisThing)
    {
	if(!thisThing.getBool("obstructed"))
	    {
		thisThing.putBool("obstructed",true);
		Room r = ((Room)thisThing.place());
		Portal way = r.getPortalByThing(thisThing);

		way.setObvious(false);
		way.backtrack().setObvious(false);
		r.tellEverybody("The keypad beeps a few times and the door closes.");
		Room or = way.sRoom();
		or.tellEverybody("The door closes quietly.");
	    }
    }
}
