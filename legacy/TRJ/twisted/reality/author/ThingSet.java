package twisted.reality.author;

import twisted.reality.*;

/**
 * <b>thing [string : key] on [local-thing : thing] to [global-thing : val]</b>
 *
 * <p>Sets thing reference value <i>key</i> on the thing <i>thing</i>
 * to <i>val</i></p>
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class ThingSet extends Verb
{
	public ThingSet()
	{
		super("thing");
	}
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing thing = d.indirectObject("on");
		Thing thing2;
		Player plr = d.subject();
		if(d.hasIndirectObject("to"))
		{
			thing2=d.indirectObject("to");
		}
		else
		{
			thing2=Age.theUniverse().findThing(d.indirectString("to"));
		}
		
		if(thing2 == null)
		{
			plr.hears("No such (global) object: " + d.indirectString("to"));
 		}
		else
		{
			thing.putThing(d.directString(),thing2);
			Object[] budgetForSubject = { "Thing Set." };
			
			Object[] budgetForOther;
			if (thing2.place() != thing.place())
			{
				Object[] bfo = 
				{
					plr, " gestures at ",thing,
					" and slowly, a gossamer thread extends away from ",
					Pronoun.obj(plr),
					", growing fainter as it stretches farther out, eventually becoming invisible."
				};budgetForOther=bfo;
			}
			else if (thing2 != thing)
			{
				Object[] bfo=
				{
					plr, " gestures from ", thing, " to ",thing2,
					" and a gossamer thread extends between them, glowing as it stretches out to wrap around them both, then growing fainter and finally invisible."
				};budgetForOther=bfo;
			}
			else
			{
				Object[] bfo=
				{
					plr, " gestures at ", thing, " and a glowing gossamer cord appears, wraps around ", Pronoun.obj(thing), ", and vanishes."
				};budgetForOther=bfo;
			}
			/* BUDGET!!! */
			d.place().tellAll(plr,budgetForSubject,budgetForOther);
		}
		return true;
	}
}
