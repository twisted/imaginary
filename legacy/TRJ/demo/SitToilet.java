package demo;

import twisted.reality.*;

public class SitToilet extends Verb
{
	public SitToilet()
	{
		super("sit");
		alias("stand");
		alias("go");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		Player p = d.subject();
		Thing toilet = d.verbObject();

		if (d.verbString().equals("sit"))
		{
			Thing box;
			if (d.hasIndirect("in"))
				box = d.indirectObject("in");
			else
				box = d.indirectObject("on");
			if (toilet != box)
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
					p.place(chair);
					p.hears(a);
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
		}
		else
		{
			if(p.place() != toilet)
				return false;
			Object[] pHears = {"You stand from the toilet, and it suddenly begins to flush and emit a loud humming sound."};
			Object[] oHear = {p," stands up from the toilet, and it begins to flush violently, with an accompanying humming sound."};
			Score.increase(p,"toilet",4);
			p.place(toilet.place());
			toilet.place().tellAll(p, pHears, oHear);
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
