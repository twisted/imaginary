package inheritance.car;

import twisted.reality.*;

// This verb intercepts any attempts to interact with
// the trunk, and fails them if you're inside the car.

public class TrunkBlock extends Verb
{
	public TrunkBlock()
	{
		super ("put");
		alias ("look");
		alias ("get");
		alias ("take");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Location trunk = (Location) d.verbObject();
		Location car = trunk.place();
		String verb = d.verbString();

		// Are they in the car?

		if (p.place() == car)
		{
			// Are they referring directly (or indirectly) to the trunk?
			
			if (d.directObject() == trunk || d.indirectObject("in") == trunk || d.indirectObject("from") == trunk)
			{	
				p.hears("You'll have to get out of the car to do that.");
				return true;
			}
		}

		return false;		
	}
}
