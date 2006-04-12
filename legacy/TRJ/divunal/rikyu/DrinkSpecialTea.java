package divunal.rikyu;

import twisted.reality.*;

public class DrinkSpecialTea extends Verb
{
	public DrinkSpecialTea()
	{
		super("drink");
		setDefaultPrep("from");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		d.subject().putFloat("health", 1.0f);
		d.subject().putFloat("stamina", 1.0f);

		Object[] subjectHears = {"You take a sip of tea from ", d.indirectObject("from"), " and suddenly feel completely refreshed."};
		Object[] othersHear = {d.subject(), " drinks from ", d.indirectObject("from"), ", and seems to stand up a little straighter."};
		
		d.subject().place().tellAll(d.subject(), subjectHears, othersHear);
		return true;
	}
}
