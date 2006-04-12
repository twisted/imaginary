package divunal.common;

import twisted.reality.*;
import java.util.Enumeration;

public class IsLit extends DynamicProperty
{
	public Object value(Thing o, Thing d)
	{
		if (! ( o instanceof Location) )
		{
			return null;
		}
		else
		{
			Location l = (Location) o;
			Enumeration e = l.things(true,true);
			if(e!=null)
			{
				while(e.hasMoreElements())
				{
					Thing t = (Thing) e.nextElement();
					if(t.getBool("isLit",o)) return Boolean.TRUE;
				}
			}
		}
		return new Boolean(false);
	}
}
