package divunal.tenth;

import twisted.reality.*;

public class SteamMeter extends DynamicProperty
{
	public Object value(Thing o, Thing d)
	{
		Thing steamsource = o.getThing("steam source");
		int i = steamsource.getInt("steam pressure");
		String descstring;
		
		descstring = "A thin metal tablet, set with a glass panel. Reflected in the glass is a fuzzy, greyish, translucent image of a circular pressure gauge whose needle is hovering around the "+i+" PSI mark.";

		return descstring;
	}
}
