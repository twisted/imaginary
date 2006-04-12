package inheritance.mummy;

import twisted.reality.*;
import java.util.*;

public class MummyHandler extends RealEventHandler
{
	public void gotEvent (RealEvent re, Thing thisThing)
	{
		Thing t = thisThing.getThing("target");
		String s = thisThing.getString("direction");
		if (t == null)
		{
			Location l = thisThing.place();
			Player p=null;
			
			Enumeration e = l.players();
			if (e!=null && e.hasMoreElements())
				p = (Player) e.nextElement();
			
			Object [] xx = {thisThing," lumbers towards ",t,"."};
			l.tellAll((Player) t,xx,xx);
		}
		else
		{
			t.handleEvent(new RealEvent("game over","The mummy eats your head.",thisThing));
		}
	}
}
