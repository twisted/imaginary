package twisted.reality.author;

import twisted.reality.*;

/**
 * This is the eventhandler which is used to clean up after the Gate
 * verb.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class GateExitKillHandler extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing t)
	{
		Room r = (Room) t;
		
		// Re-describe it.
		
		String[] x = (String[]) e.arg();
		
		r.removeDescriptor(x[1]);
		r.removePortal(x[0]);
		
		r.tellEverybody("The gate which led "+x[0]+"ward suddenly vanishes in a burst of sparks.");
		r.removeHandler("gate");
		r.removeProp("gate active");
	}
}
