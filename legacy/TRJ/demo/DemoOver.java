package demo;

import twisted.reality.*;

public class DemoOver extends RealEventHandler
{
	public void gotEvent(RealEvent re, Thing thisThing)
	{
		Player dead = (Player) thisThing;
		StringBuffer sb = new StringBuffer(String.valueOf(re.arg())+"\n");
		int score = dead.getInt("score");
		int scoremax = dead.getInt("score max");
		
		sb.append("***** You have died. *****\nThank you for playing with the Twisted Reality Demo Center.  Your score was "+score+" out of a possible "+scoremax+", ranking you as a `guest'.");
		
		dead.alert(sb.toString());
		
		if (!dead.isGod())
		{
			Age.theUniverse().disconnect(dead);
		}
	}
}
