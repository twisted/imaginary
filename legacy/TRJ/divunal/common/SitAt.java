package divunal.common;

import twisted.reality.*;

// This is for sitting "at" things, like desks
// and computer terminals.

public class SitAt extends Verb
{
	public SitAt()
	{
		super("sit");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		Thing box;
		if (d.hasIndirect("at"))
			box = d.indirectObject("at");
		else
			box = d.indirectObject("on");
		
		Location desk;
		if ((box instanceof Location) && (desk=((Location)box)).isBroadcast())
		{
			if (hasRoom(desk))
			{
				d.subject().place(desk);
				Object[] sitdesk = {"You sit at ",desk,"."};
				d.subject().hears(sitdesk);
			}
			else
			{
				d.subject().hears("There's no room to sit there.");
			}
		}
		else
		{
			d.subject().hears("There's nowhere to sit there.");
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
