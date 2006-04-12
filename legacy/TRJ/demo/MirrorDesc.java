package demo;

import twisted.reality.*;

public class MirrorDesc extends DynamicProperty
{
	public Object value(Thing o, Thing d)
	{
		String descstring;
		
		descstring = o.getString("base description")+d.fullyDescribeTo(d);
		
		return descstring;
	}
}
