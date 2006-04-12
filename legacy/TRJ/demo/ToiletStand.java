package demo;

import twisted.reality.*;

import java.util.Enumeration;

public class ToiletStand extends Verb
{
	public ToiletStand()
	{
		super("stand");
		alias("go");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		Player p = d.subject();
		Location toilet = (Location) d.verbObject();
		
		if(p.place() != toilet)
			return false;
		Object[] pHears = 
		{"You stand from the toilet, and it suddenly begins to flush and emit a loud humming sound."};
		Object[] oHear = 
		{p," stands up from the toilet, and it begins to flush violently, with an accompanying humming sound."};
		
		Score.increase(p,"toilet",4);
		
		p.place(toilet.place());
		
		toilet.place().tellAll(p, pHears, oHear);
		
		Enumeration e = toilet.things(false);
		while (e.hasMoreElements())
		{
			Thing t = (Thing) e.nextElement();
			if (t.getBool("romero"))
			{
				t.handleEvent("gib",null,p);
			}
			else
			{
				Location fountain = (Location)toilet.getThing("fountain");
				t.place(fountain);
				/* a descriptive message, perhaps? */
			}
		}
		return true;
	}
}
