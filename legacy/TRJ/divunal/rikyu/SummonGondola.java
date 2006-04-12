package divunal.rikyu;

import twisted.reality.*;

public class SummonGondola extends Verb
{
	public SummonGondola()
	{
		super("ring");
		alias("take");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if(d.verbString().equals("take"))
			return false;
		
		Location gondola;
		
		Object[] subjectHears = {"You ring ", d.verbObject()};
		Object[] othersHear   = {d.subject(), " rings ", d.verbObject()};
		d.subject().place().tellAll(d.subject(), subjectHears, othersHear);
			
		try
		{
			gondola = (Location)Age.theUniverse().findThing("gondola");
		}
		catch(ClassCastException e){ return false; }
		
		if(gondola.things().hasMoreElements())
		{
			Object[] sorry = {"Sorry, ", gondola, " is in use right now."};
			d.subject().hears(sorry);
		}
		else if(gondola.place() != d.subject().topPlace())
		{
			Object[] leaving = {gondola, " has been requested elsewhere."};
			Object[] entering = {gondola, " drifts in, ready for use."};
			gondola.moveTo(d.subject().place(), leaving, entering);
		}
		return true;
	}
}
