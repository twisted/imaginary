package twisted.reality.plugin;

import java.util.*;
import twisted.reality.*;

/**
 * This is a sample handler. It makes whatever room you enable it on
 * say "A disembodied voice says ``Time has passed''" every once in a
 * while.  It's a good primer in how to do looped events.  It uses the
 * standard 'say' handler. (To see how it does it, peek at the source
 * to the PlayerSayHandler, which does unexpected things if nobody's
 * actually speaking... It should be enabled under the event title
 * "startup".
 * 
 * @version 1.0.0, 15 Jun 1998
 * @author Glyph Lefkowitz
 */

public class RoomSayHandler extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		((Location) thisThing).broadcastEvent
			(new RealEvent("say","Time has passed.",null));
		thisThing.handleDelayedEvent(new RealEvent("startup",null,null),1);
	}
}
