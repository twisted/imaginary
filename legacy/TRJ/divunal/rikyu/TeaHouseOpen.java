package divunal.rikyu;

import twisted.reality.*;

public class TeaHouseOpen extends Verb
{
	public TeaHouseOpen()
	{
		super("enter");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Room tea = (Room)Age.theUniverse().findThing("Tea House");
		if(d.verbString().equals("enter"))
		{
			if(qualifies(d.subject()))
			{
				Object[] heard = {d.subject(), " enters the tea house."};
				Object[] subjectHears = {"You enter the tea house."};
				d.subject().hears(subjectHears);
				d.subject().removeProp("washed");
				d.subject().removeProp("drank");
				d.subject().moveTo(tea, heard);
			}
			else
			{
				Thing ghost = Age.theUniverse().findThing("ghastly specter");
				Object[] leave = {"The ghastly specter vanishes as quickly as it appeared."};
				Object[] arrive = {"A ghastly specter swoops down from the sky."};
				ghost.moveTo(d.subject().place(), leave, arrive);
				
				Object[] theyHear = {d.subject(), " attempts to enter the tea house."};
				d.subject().place().tellAll(theyHear);
				Object[] theyHear2 = {ghost, " says: \"You, ", d.subject(), " are forbidden to enter this tea house!\""};
				d.subject().place().tellAll(theyHear2);
				
				ghost.moveTo(null, leave, arrive);
			}
		}
		else
		{
			return false;
		}
		return true;
	}
	
	private boolean qualifies(Player p)
	{
		if(! p.getBool("drank"))
			return false;
		if(! p.getBool("washed"))
			return false;
		if(Age.theUniverse().findThing("tied stone").topPlace() == p.topPlace())
			return false;
		return true;
	}
}
