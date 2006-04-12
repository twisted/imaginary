package divunal.common.author;

import twisted.reality.*;

public class SayBox extends RealEventHandler
{
	public void gotEvent(RealEvent e,
						 Thing thisThing)
	{
		if(e.arg().equals("transport"))
		{
			if(thisThing.place()==e.origin())
			{
				Thing t = thisThing.place();
				if(t instanceof Player) 
				{
					Player p = (Player) t;
					p.hears("You feel yourself being whisked away, as by a strong wind... you drop something.");
					thisThing.place((Location) thisThing.getThing("magic box location"));
					p.place((Location) thisThing.getThing("magic box target"));
					
				}
				else
				{
					Age.log("Things who aren't people, talking, saying transport, while holding a box. This is probably not supposed to happen, look into it.");
				}
			}
		}
	}
}
