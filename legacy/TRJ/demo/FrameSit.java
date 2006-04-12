package demo;

import twisted.reality.*;

/**
 * This is for sitting on (or in) chairs and other
 * sittable objects that are Giant Robot sized.
 * 
 * @author Tenth */

public class FrameSit extends Verb
{
	public FrameSit()
	{
		super("sit");
	}

	public boolean action (Sentence d) throws RPException
	{
		Thing box;
		Player p = d.subject();
		Thing g = p.place();

		if (d.hasIndirect("in"))
			box = d.indirectObject("in");
		else
			box = d.indirectObject("on");
		if (d.verbObject() != box)
			return false;

		if (!g.getBool("is guymelef"))
		{
			Object[] pHears = {d.verbObject(), " is too tall for you to get onto, much less comfortable to sit in."};
			p.hears(pHears);
			return true;
		}

		Location chair;
		if ((box instanceof Location) && (chair=((Location)box)).isBroadcast())
		{
			if (hasRoom(chair))
			{
				//added by guyute
				String prep = chair.getString("preposition");
				//end add
				Object[] a = {"You sit " + prep + " ",chair,"."};
				Object[] b = {g, " lowers itself into ", chair, "."};
				chair.place().tellAll(p, a, b);
				g.place(chair);
				p.setFocus(chair.place());
			}
			else
			{
				p.hears("There's no room to sit on that.");
			}
		}
		else
		{
			p.hears("There's no good surface to sit on that.");
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
