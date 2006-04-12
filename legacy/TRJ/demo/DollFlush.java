package demo;

import twisted.reality.*;
import java.util.Enumeration;

public class DollFlush extends RealEventHandler
{
	public void gotEvent(RealEvent re, Thing thisThing)
	{
		Player scorer = (Player) re.origin();
		int counter = thisThing.getInt("romero counter");
		if (counter == 0)
		{
			counter++;
			Object[] xxx = {
				thisThing," begins spinning madly in the toilet, eventually getting stuck.  The sound producing mechanism seems to jam, and you hear a stream of high-speed babble.  The word \"giblets\" is mentioned several times in the squeaky litany."
			};
			thisThing.putInt("romero counter",counter);
			
			thisThing.topPlace().tellAll(xxx);
			thisThing.handleDelayedEvent(re,1);
		}
		else
		{
			thisThing.removeProp("romero counter");
			Enumeration enum = thisThing.topPlace().players();
			Portal pl = ((Room) thisThing.topPlace()).getPortal("west");
			Thing dr = pl.sThing();
			boolean dro = dr.getBool("obstructed");
			Location l2 = pl.sRoom();
			boolean givefull = true;
			boolean givescore = true;

			if (dro)
			{
				while(enum.hasMoreElements())
				{
					Player p = (Player) enum.nextElement();
					if (p == scorer) givescore=false;
					p.handleEvent("demo over","You realize that the doll is going to explode; a bit late, as white-hot plastic shrapnel pins you against the closed door of the bathroom stall.  Your remains are instantly and automatically sanitized for your protection, thanks to the Frobozz Magic Zero-Gravity Guest Corpse Removal Device.",p);
				}
			}
			else
			{
				while (enum.hasMoreElements())
				{
					Player p = (Player) enum.nextElement();
					if (p == scorer) givefull=false;
					Object[] fh = {
p,"flies out of the room."
					};
					Object[] rh = {
p,"flies out of the bathroom stall and lands in a heap on the floor."
					};
					p.moveTo(l2,fh,rh);
				}
			}
			if (givescore)
			{
				int i = 20;
				if (givefull) i += 20;
				Score.increase(scorer,"romero",i);
			}
		}
	}
}
