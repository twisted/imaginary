package divunal.rikyu;

import twisted.reality.*;

public class TeaHouseDrink extends Verb
{
	public TeaHouseDrink()
	{
		super("drink");
		setDefaultPrep("from");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		d.subject().putBool("drank", true);
		
		Object[] subjectHears = {"You cup your hands and drink from ", d.indirectObject("from")};
		Object[] othersHear = {d.subject(), " cups ", Name.of("hands", d.subject()) , " and drinks from ", d.indirectObject("from")};
		
		d.subject().place().tellAll(d.subject(), subjectHears, othersHear);
		return true;
	}
}
