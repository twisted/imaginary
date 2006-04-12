package twisted.reality.plugin;

import twisted.reality.*;

public class Login extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		Player plr = (Player) thisThing;
		
		Location l = ((Location)plr.getThing("oldlocation"));
		Object[] mtm = {plr, " wanders in."};
		plr.moveTo(l,mtm);
	}
}
