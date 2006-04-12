package twisted.reality.plugin.furniture;

import twisted.reality.*;

/**
 * This is for lying on (or in) beds and other
 * lieable objects.
 * 
 * @author Glyph */

public class Lie extends Verb
{
	public Lie()
	{
		super("lie");
		alias("lay");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		Thing box;
		if (d.hasIndirect("on"))
			box = d.indirectObject("on");
		else
			box = d.indirectObject("in");
		
		Location bed;
		if ((box instanceof Location) && (bed=((Location)box)).isBroadcast())
		{
			if (hasRoom(bed))
			{
				d.subject().place(bed);
				Object[] laydown = {"You lay down on ", bed,"."};
				d.subject().hears(laydown);
			}
			else
			{
				d.subject().hears("There isn't enough room.");
			}
		}
		else
		{
			d.subject().hears("There's nowhere to lay down there.");
		}
		return true;
	}
	boolean hasRoom(Location  l)
	{
		int maxOccupancy = l.getInt("maximum occupancy");
		int curOccupancy = l.thingCount();
		return (maxOccupancy>curOccupancy);
	}
}
