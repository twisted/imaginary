package demo;

import twisted.reality.*;

public class DemoKnobTurn extends Verb
{
	public DemoKnobTurn()
	{
		super("turn");
		alias("twist");
		alias("rotate");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing knob = d.directObject();
		Player p = d.subject();
		Room r = (Room) knob.place();
		int degree;
		String dse;
		String dir;
		if (d.hasIndirect("to"))
			dse = d.indirectString("to");
		else
			dse = d.directString();

		if (dse.endsWith("left") || dse.equals("left"))
			dir = "left";
		else if (dse.endsWith("right") || dse.equals("right"))
			dir = "right";
		else
		{
			Object[] pDumb = {"Perhaps turning it to the left or right might be more appropriate."};
			Object[] oDumb = {p," tugs on the knob."};
			
			r.tellAll(p, pDumb, oDumb);
			return true;
		}

		Object[] pNoTurn = {"You can't turn the knob any further."};
		Object[] oNoTurn = {p," wrestles with the knob for a moment."};

		Object[] pTurn = {"You turn the knob to the ",dir,"."};
		Object[] oTurn = {p," turns the knob to the ",dir,"."};

		degree = knob.getInt("degree");

		if (dir.equals("left"))
		{
			if (degree > -2)
			{
				degree -= 1;
				r.tellAll(p, pTurn, oTurn);
				Score.increase(p,"sink",32);
			}
			else
			{
				r.tellAll(p, pNoTurn, oNoTurn);
				return true;
			}
		}
		else if (dir.equals("right"))
		{
			if (degree < 2)
			{
				degree += 1;
				r.tellAll(p, pTurn, oTurn);
			}
			else
			{
				r.tellAll(p, pNoTurn, oNoTurn);
				return true;
			}
		}

		knob.putInt("degree",degree);

		if (degree != 0)
			r.putDescriptor("water","The sound of trickling water echos from the sink.");
		else
			r.removeDescriptor("water");


		switch(degree)
		{
		case -2:
			r.tellEverybody("Water spurts violently from the faucet.");
			knob.putDescriptor("water","It is spraying cold water into the sink at an impressive pace.");
			break;
		case -1:
			r.tellEverybody("Water begins to dribble from the faucet.");
			knob.putDescriptor("water","A trickle of cold water is running from it into the sink.");
			break;
		case 0:
			r.tellEverybody("Water ceases to flow from the faucet.");
			knob.removeDescriptor("water");
			break;
		case 1:
			r.tellEverybody("Water begins to dribble from the faucet.");
			knob.putDescriptor("water","A stream of warm water runs from the faucet into the sink.");
			break;
		case 2:
			r.tellEverybody("Water sprays violently from the faucet.");
			knob.putDescriptor("water","It is spraying steaming hot water into the sink."); 
			break;
		}
		
		return true;
	}
}
