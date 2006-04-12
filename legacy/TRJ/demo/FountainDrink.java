package demo;

import twisted.reality.*;

/**
 * This is the disturbing verb for the drinking fountain.
 *
 * @author Tenth */

public class FountainDrink extends Verb
{
	public FountainDrink()
	{
		super ("drink");
	}

	public boolean action(Sentence d) throws RPException
	{
		Thing fount = d.verbObject();
		Player p = d.subject();

		if (d.hasDirect())
		{
			if (d.directObject() == fount)
			{
				drinkWater(p, fount);
				return true;
			}
		}
		else if (d.hasIndirect("from"))
		{
			if (d.indirectObject("from") == fount)
			{
				drinkWater(p, fount);
				return true;
			}
		}

		return false;
	}

	public static void drinkWater(Player p, Thing f)
	{
		if (!f.getBool("spouting water"))
		{
			Object[] phears = {f, " is not producing any water for you to drink."};
			p.hears(phears);
			return;
		}

		String[] speech = 
		{
			"drinking from a cold mountain stream",
			"skiing down an arctic mountain",
			"sailing through artic waters"
		};

		String[] getLife = 
		{
			"freezing to death on the set of a breathmint commercial",
			"repeatedly drinking water",
			"weren't so much of a loser that you spent most of your time drinking from a fountain."
		};

		int drinks = p.getInt("drinking problem");
		String message;

		if (drinks < 4)
		{
			drinks += 1;
			message = random(speech);
			p.putInt("drinking problem", drinks);
		}
		else
		{
			message = random(getLife);
			p.removeProp("drinking problem");
		}

		Object[] pHears = {"You take a drink of cool, refreshing water from ",f," and feel refreshed and invigorated, as if you were ",message,"..."};
		Object[] oHears = {p, " drinks from the fountain."};

		p.place().tellAll(p, pHears, oHears);
	} 

}
