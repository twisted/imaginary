package twisted.reality.plugin;

import java.util.*;
import twisted.reality.*;

/**
 * This is the event handler that all player/characters should be
 * equipped with, allowing their character to detect and display "say"
 * events. 
 *
 * You could disable or replace this to make players deaf, although we
 * don't currently have any way to segregate audible stuff out of
 * p.hears() calls, and doing that would be a pain anyway. And clever
 * players could always put messages into emotes... Oh well.
 * 
 * @author Probably Glyph */

public class PlayerSayHandler extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		Player p = (Player) thisThing;
		String s = (String) e.arg();
		Thing t = e.origin();
		
		if (t==null)
			p.hears("A disembodied voice says: \""+s+"\"");
		else if(p!=t)
		{
			Object[] xxx = {t," says: \""+s+"\""};
			p.hears(xxx);
		}
		else
			p.hears("You say: \""+s+"\"");
	}
}
