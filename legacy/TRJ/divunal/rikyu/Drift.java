package divunal.rikyu;

import twisted.reality.*;

public class Drift extends Verb
{
	public Drift()
	{
		super("drift");
		alias("pass");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Room room = (Room)d.subject().topPlace();
		Room nextRoom = room.toThe(d.directString());
		
		if(nextRoom != null)	
		{
			Object[] leave = {d.subject(), " drifts ", d.directString(), "."};
			Object[] arrive = {d.subject(), " drifts in."};// from the ", d.directString}
			
			d.subject().moveTo(nextRoom, leave, arrive);
			
			Object[] hears = {"You drift ", d.directString(), "."};
			return true;
		}
		else
		{
			return false;
		}
	}
}
