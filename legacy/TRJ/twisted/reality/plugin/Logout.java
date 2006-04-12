package twisted.reality.plugin;

import twisted.reality.*;

/**
 * This demonstrates a sample "logout" behavior for the Pump.  It
 * removes the player from the accessible map (places them at null)
 * and stores their old location so it can be restored when they next
 * log in.
 */

public class Logout extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		Thing plc = thisThing.place();
		if (plc != null)
		{
			thisThing.putThing("oldlocation",plc);
			Object[] mtm = {thisThing," wanders off."};
			thisThing.moveTo(null,mtm);
		}
	}
}
