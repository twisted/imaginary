package divunal.common.author;

import twisted.reality.*;

public class TakeBox extends RealEventHandler
{
	public void gotEvent(RealEvent e,
						 Thing thisThing)
	{
		if(e.origin() instanceof Player)
		{
			Player p = (Player)e.origin(); 
			p.hears("The box appears to be glowing and a small ticking sound radiates out from the hole in the middle.");
			thisThing.putThing("magic box player",p);
			thisThing.handleDelayedEvent(new RealEvent("magic box return", p, thisThing),20);
		}
		else if(e.origin() != thisThing.getThing("magic box location"))
		{
			Object[] exitMessage = 
			{
				thisThing,
				"vanishes in a burst of frenzied ticking."
			};
			Object[] enterMessage =
			{
				"There is a popping sound as ",thisThing,"appears."
			};
			thisThing.moveTo( (Location) thisThing.getThing("magic box location"),
							  exitMessage,enterMessage);
		}
	}
}
