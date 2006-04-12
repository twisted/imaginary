package demo;

import twisted.reality.*;

public class Score
{
	public static void increase(Player p, String identifier, int amount)
	{
		if (p.getBool("score init") && !p.getBool("score point "+identifier))
 		{
			int currentScore = p.getInt("score");
			currentScore += amount;
			int scoreMax = p.getInt("score max");
			p.putInt("score",currentScore);
			p.putBool("score point "+identifier,true);
			if(amount > 0)
			{
				p.hears("[Your score has gone up by "+amount+".  It is now "+currentScore+" out of a possible "+scoreMax+".]");
			}
			else
			{
				p.hears("[Your score has gone down by "+(-amount)+".  It is now "+currentScore+" out of a possible "+scoreMax+".]");
			}
		}
	}
	
	public static void init(Player p, int start, int max)
	{
		p.putInt("score",start);
		p.putInt("score max",max);
		p.putBool("score init",true);
		p.hears("[Your score is "+start+" out of a possible "+max+".]");
	}
}
