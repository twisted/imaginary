package divunal.rikyu;

import twisted.reality.*;
import divunal.common.*;
import java.util.Vector;
import java.util.Enumeration;

public class Spy extends Skill
{
	public Spy()
	{
		super("spy");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing t = Age.theUniverse().findThing(d.indirectString("on"));
		
		Vector subjectHears = new Vector();
		subjectHears.addElement("You open your third eye, and attempt to visualize ");
		subjectHears.addElement(t);
		
		d.subject().hears(subjectHears);
		
		if(t.getBool("noSpy") && (! d.subject().isGod()))
		{
			subjectHears.removeAllElements();
			subjectHears.addElement("Your mind is pushed back by a force of some sort.");
			d.subject().hears(subjectHears);
			return true;
		}
		
		subjectHears.removeAllElements();
		
		if(t.place() == null && !(t instanceof Location))
		{
			subjectHears.addElement("That's a very poor thing to spy on.");
		}
		else if(t.place() != null)
		{
			subjectHears.addElement("You see ");
			subjectHears.addElement(t);
			subjectHears.addElement(" in ");
			subjectHears.addElement(t.place());
			subjectHears.addElement(".\n");
		}

		subjectHears.addElement("\n" + t.DESC() + "\n");
		if(t instanceof Location)
		{
			subjectHears.addElement("The contents of ");
			subjectHears.addElement(t);
			subjectHears.addElement(" are ");
			
			int preSize = subjectHears.size();
			
			Enumeration things = ((Location)t).things();
			while(things.hasMoreElements())
			{
				Thing theThing = (Thing)things.nextElement();
				if(t.isComponent() && (!d.subject().isGod()))
						continue;
				if( (! things.hasMoreElements()) && subjectHears.size() > preSize)
					subjectHears.addElement("and ");

				subjectHears.addElement(theThing);

				if(things.hasMoreElements())
					subjectHears.addElement(", ");
				else
					subjectHears.addElement(".");
			}
		}
		d.subject().hears(subjectHears);
		return true;
	}
	
	public boolean learnSkill(Player p)
	{
		String sname = skillName();

		// If the player's base psyche sucks,
		// They can't learn this ability.

		if (p.getFloat("psyche") < 0.3f)
		{
			p.hears("You just can't seem to understand the idea...");
			return false;
		}

		if (p.getFloat(sname) != 0)  // You can't learn it twice. :)
		{
			p.hears("You've already learned that technique.");
			return false;
		}

		// Since you're learning it, be sure to make it not be zero anymore.
		p.putFloat(sname, 0.1f);
		return true;
	}
	
	public boolean teachable(){ return true; }
	public String relevantStat() {return "psyche";}
}
