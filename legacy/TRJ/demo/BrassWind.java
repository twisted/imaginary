package demo;

import twisted.reality.*;

public class BrassWind extends Verb
{
	public BrassWind()
	{
		super("wind");
		alias("unlock");
		alias("lock");
		setDefaultPrep("with");
	}
    
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Thing windee = d.directObject();
		int winds = windee.getInt("winds");
		Location room = d.place();
		boolean windable = windee.getBool("windable");
		
		if (windable == false)
		{
			Object[] unwindable={"You can't wind ",windee,"."};
			p.hears(unwindable);
			return true;
		}
		
		if (winds < 15)
		{
			Object[] windsIt={p," winds ",windee,"."};
			Object[] windIt={"You wind ",windee,"."};
			room.tellAll(p,windIt,windsIt);
			demo.Score.increase(p,"roach",8);
			if (winds == 0)
				windee.handleDelayedEvent(new RealEvent("startup",null,null),1);
			winds += 5;
			windee.putInt("winds",winds);
			windee.mood(null);
		}
		else
		{
			Object[] attWinds = {p, " attempts to wind ", windee, "."};
			Object[] attWind = {"You attempt to wind ", windee, " but it is already wound as tightly as possible."};
			room.tellAll(p,attWind,attWinds);
		}
		return true;
	}
}
