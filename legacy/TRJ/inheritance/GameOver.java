package inheritance;

import twisted.reality.*;

public class GameOver extends RealEventHandler
{
	public void gotEvent(RealEvent re, Thing thisThing)
	{
		Player dead = (Player) thisThing;
		dead.hears("\n"+String.valueOf(re.arg())+"\n");
		if (dead.isGod())
		{
			dead.hears("***** You have(n't really) died. *****");
			dead.hears("Continue on...");
		}
		else
		{
			dead.hears("***** You have died. *****");
			dead.hears("Would you like to RESTART, RESTORE, or QUIT?");
		}
	}
}
