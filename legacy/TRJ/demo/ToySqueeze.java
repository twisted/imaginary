package demo;

import twisted.reality.*;

public class ToySqueeze extends Verb
{
	public ToySqueeze()
	{
		super("squeeze");
		alias("squeak");
		alias("squeek");
	}
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Location l = d.place();
		Thing theDoll = d.directObject();
		String v = d.verbString();

		if (theDoll.place() != p)
		{
			p.hears("You don't have it.");
			return true;
		}

		Score.increase(p,"Bun-Bun",16);

		if (d.hasIndirect("at"))
		{
			Thing victim = d.indirectObject("at");
			
			if (victim == p)
			{
				Object[] pssHears = {"You point ",theDoll," at your head and give it a good squeak, and stagger backwards from the ear-shattering *SQUEAK* that results."};
				Object[] ossHears = {p, " points ",theDoll," at ",Pronoun.of(p)," head and squeezes it, staggering backwards from the deafening squeak it produces."};
				l.tellAll(p, pssHears, ossHears);
			}
			else
			{
				Object[] psaHears = {"You point ",theDoll," at ",victim," and give ",Pronoun.obj(victim)," a good squeak."};
				Object[] tsaHears = {p, " points ",theDoll," at you and squeezes it, producing a high pitched, ear-shattering *SQUEEK*!"};
				Object[] osaHears = {p, " points ",theDoll," at ",victim," and gives ",Pronoun.obj(victim)," a good squeek."};
				l.tellAll(p, victim, psaHears, tsaHears, osaHears);
			}
		}
		else
		{
			Object[] psHears = {"You give ",theDoll," a good squeeze, and it emits a deafening *SQUEEK*!"};
			Object[] osHears = {p, " squeezes ",theDoll,", and it emits a deafening *SQUEEK*!"};
			l.tellAll(p, psHears, osHears);
		}
		return true;
	}
}
