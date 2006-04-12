package divunal.common.author;

import twisted.reality.*;

public class VoiceTeleport extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		Thing p = e.origin();
		
		Thing t = thisThing.getThing("teleport phrase "+e.arg());
		
		if(t != null)
		{
			p.place((Location)t);
		}			
		// bye
	}
}
