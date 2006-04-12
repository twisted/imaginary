package twisted.reality.plugin.furniture;

import twisted.reality.*;

/**
 * This is for sitting on (or in) chairs and other
 * sittable objects.
 * 
 * @author Glyph */

public class Sit extends Verb
{
	public Sit()
	{
		super("sit");
	}

	public boolean action (Sentence d) throws RPException
	{
		Thing box;
		if (d.hasIndirect("in"))
			box = d.indirectObject("in");
		else
			box = d.indirectObject("on");
		if (d.verbObject() != box)
			return false;
		Location chair;
		if ((box instanceof Location) && (chair=((Location)box)).isBroadcast())
		{
			if (hasRoom(chair))
			{
				//added by guyute
				String prep = chair.getString("preposition");
				//end add
				Object[] a = {"You sit " + prep + " ",chair,"."};
				d.subject().place(chair);
				d.subject().hears(a);
			}
			else
			{
				d.subject().hears("There's no room to sit on that.");
			}
		}
		else
		{
			d.subject().hears("There's no good surface to sit on that.");
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
