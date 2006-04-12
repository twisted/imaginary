package inheritance.car;

import twisted.reality.*;

// This is a generic Open/Close verb for
// containers.

public class CarEnterLeave extends Verb
{
	public CarEnterLeave()
	{
		super ("enter");
		alias ("board");
		alias ("exit");
		alias ("leave");
		alias ("get");
		alias ("go");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Location car = (Location) d.verbObject();
		Player p = d.subject();
		Location room = d.place();
		String verb = d.verbString();

		if (verb.equals("go"))
		{
			if (p.place() == car)
				getOutOfCar(p, car);
			else
				return false;
		}

		if (verb.equals("get"))
		{
			if (d.hasIndirect("in"))
			{
				if (d.indirectObject("in") == car)
				{
					getIntoCar(p, car);
					return true;
				}
			}
			String dds = d.directString();
			if (dds.startsWith("out"))
			{
					getOutOfCar(p, car);
					return true;
			}
			return false;
		}

		if (verb.equals("enter") || verb.equals("board"))
		{
			if (d.directObject() == car)
			{
				getIntoCar(p, car);
			}
			else
				return false;
		}
		else
		{
			getOutOfCar(p, car);
		}

		return true;
	}

	public void getIntoCar(Player p, Location car)
	{
		if (!(car.areContentsOperable()))
		{
			p.hears("The car door is closed.");
		}		
		else if (p.place() == car)
		{
			p.hears("You're already inside the car...");
		}
		else
		{
			Object[] pGetsIn = {"You get into ",car,"."};
			Object[] moveString = {p," gets into the car."};
			p.hears(pGetsIn);
			p.moveTo(car, moveString);
			p.setFocus(car);
		}
	}

	public void getOutOfCar(Player p, Location car)
	{
		if (!(car.areContentsOperable()))
		{
			p.hears("The car door is closed.");
		}
		else if (!(p.place() == car))
		{
			p.hears("You aren't in the car...");
		}
		else
		{
			Object[] pGetsOut = {"You get out of ",car,"."};
			Object[] moveString = {p," gets out of the car."};
			p.hears(pGetsOut);
			p.moveTo(car.place(), moveString);
			p.setFocus(p.place());
		}
	}
}
