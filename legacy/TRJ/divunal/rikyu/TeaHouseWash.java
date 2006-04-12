package divunal.rikyu;

import twisted.reality.*;

public class TeaHouseWash extends Verb
{
	public TeaHouseWash()
	{
		super("wash");
		setDefaultPrep("in");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		d.subject().putBool("washed", true);
		
		Object[] subjectHears = {"You wash your hands in ", d.indirectObject("in")};
		Object[] othersHear = {d.subject(), " washes ", Name.of("hands", d.subject()) , " hands in ", d.indirectObject("in")};
		
		d.subject().place().tellAll(d.subject(), subjectHears, othersHear);
		return true;
	}
}
