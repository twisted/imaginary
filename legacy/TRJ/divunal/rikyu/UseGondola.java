package divunal.rikyu;

import twisted.reality.*;

public class UseGondola extends Verb
{
	public UseGondola()
	{
		super("enter");		
		alias("leave");
		alias("exit");		
		alias("paddle");
		alias("go");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		//if(d.hasDirect() && d.directObject() != d.verbObject())
		//	return false;
		if(d.verbString().equals("enter"))
		{
			if(d.subject().place() == d.verbObject())
			{
				Object[] subjectHears = {"You're already in ", d.verbObject()};
				d.subject().hears(subjectHears);
				return true;
			}
			Object[] subjectHears = {"You enter ", d.verbObject()};
			d.subject().hears(subjectHears);
			Object[] moveText = {d.subject(), " enters ", d.verbObject()};
			d.subject().moveTo((Location)d.verbObject(), moveText);
		}
		else if(d.verbString().equals("exit") || d.verbString().equals("leave"))
		{
			if(d.subject().place() != d.verbObject())
			{
				Object[] subjectHears = {"Um, you aren't in ", d.verbObject()};
				d.subject().hears(subjectHears);
				return true;
			}
			else if(d.subject().topPlace().getBool("needsBoat"))
			{
				Object[] subjectHears = {"You can't leave ", d.verbObject(), "! There's nowhere to go!"};
				d.subject().hears(subjectHears);
				return true;
			}
			Object[] subjectHears = {"You exit ", d.verbObject()};
			d.subject().hears(subjectHears);
			Object[] moveText = {d.subject(), " exits ", d.verbObject()};
			d.subject().moveTo(d.verbObject().topPlace(), moveText);
		}
		else if(d.verbString().equals("paddle") || d.verbString().equals("go"))
		{
			if(d.subject().place() != d.verbObject())
			{
				Object[] subjectHears = {"Um, you aren't in ", d.verbObject()};
				d.subject().hears(subjectHears);
				return true;
			}
			
			Room theRoom = (Room)d.subject().topPlace();
			Room toRoom = theRoom.toThe(d.directString());
			
			if(toRoom == null ||
			       theRoom.getPortal(d.directString()).sThing() == null ||
			       (! theRoom.getPortal(d.directString()).sThing().getBool("wateryExit"))   )
			{
				Object[] subjectHears = {"The water doesn't go that way."};
				d.subject().hears(subjectHears);
				return true;
			}
			Object[] newHears = {d.verbObject(), " has arrived from the ", Portal.reverse(d.directString()), "."};
			Object[] oldHears = {d.verbObject(), " has exited to the ", d.directString()};
			d.verbObject().moveTo(toRoom, newHears, oldHears);
		}
		else
		{
			return false;
		}

		return true;
	}
}
