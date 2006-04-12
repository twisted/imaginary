package divunal.common.skills;

import twisted.reality.*;
import java.util.Vector;
import divunal.Divunal;

public class ReadAura extends Verb
{
    public ReadAura()
    {
		super("aura");
		alias("scan");
    }
    
    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		Location l = d.place();
		Thing target = d.directObject();
		boolean isPlayer = (target instanceof Player);
		Vector aurastring=new Vector();
		Player targetp;
		if (isPlayer) 
			targetp = (Player) target;
		else
			targetp = null;
		float tempstat;

		// Inform the room that the player is staring at something

		float result = Divunal.weightedPsycheCheck(p, 0.5f);

		if (result < 0)
		{
			p.hears(random(readAuraFailure));
			if (isPlayer)
			{
				Object[] tph = {p,random(auraFailureVerb)," at you."};
				targetp.hears(tph);
			}
			else
			{
				Object[] eeh = {p,random(auraFailureVerb)," at ",targetp,"."};
				/*l.tellEverybodyBut(p, p.name()+random(auraFailureVerb)+" at "+targetp.the()+target.name()+".");*/
				l.tellAll(p,null,eeh);
			}
			return true; // I'm exiting 'cause I failed
		}

		// You just screwed up, and it was obvious

		if (result < 0.8)
		{
			Object[] obvious={p,random(auraPassVerb)," at ",target,"."};
			if (isPlayer)
			{
				Object[] eeh = {p,random(auraFailureVerb)," at ",targetp,"."};
				d.place().tellAll(d.subject(),targetp,null,eeh,obvious);
			}
			else
			{
				d.place().tellAll(d.subject(),null,obvious);
			}
		}
		
		// You succeeded, and it was obvious.

		//Otherwise, you succeeded, and it was subtle.

		if (aurastring.size()!=0)
		{
			p.hears(aurastring);
			return true;
		} 
		// If this thing has a special Aura string, display that instead

		if (!(isPlayer))
		{
			Object[] deepwithin={"You look deep within ",target,", but ",Pronoun.of(target)," is cold and empty."};
			p.hears(deepwithin);
			return true;
		}
		// If it doesn't have a psyche to work with, and has no aura, you
		// don't see one.  :-)

		// Now for the fun part;

		aurastring.addElement(targetp.name());
		aurastring.addElement(" is surrounded by a ");

		tempstat = Divunal.stamina(targetp);

		if (tempstat < -0.3)
			aurastring.addElement("pale, sickly ");
		else if (tempstat < 0)
			aurastring.addElement("weak ");
		else if (tempstat < 0.3)
			aurastring.addElement("soft ");
		else if (tempstat < 0.7)
			aurastring.addElement("bright ");
		else
			aurastring.addElement("brilliant ");

		tempstat = targetp.getFloat("memory");

		if (tempstat < -0.3)
			aurastring.addElement("purple ");
		else if (tempstat < 0)
			aurastring.addElement("red ");
		else if (tempstat < 0.3)
			aurastring.addElement("blue ");
		else if (tempstat < 0.7)
			aurastring.addElement("light blue ");
		else
			aurastring.addElement("white ");

		aurastring.addElement("glow, ");

		tempstat = targetp.getFloat("psyche");

		if (tempstat > 0)
		{
			if (tempstat < 0.3)
				aurastring.addElement("with faint trailing streaks. ");
			else if (tempstat < 0.5)
				aurastring.addElement("with thin, radiating lines. ");
			else if (tempstat < 0.7)
				aurastring.addElement("with bright, radiating tendrils. ");
			else
				aurastring.addElement("casting brilliant, shining beams. ");
		}
		
		tempstat = targetp.getFloat("violence");

		if (tempstat > 0)
		{
			if (tempstat < 0.2)
				aurastring.addElement("It is tainted by a few dark, unhealthy patches, and ");
			else if (tempstat < 0.4)
				aurastring.addElement("It is streaked and stained by dark, threatening patterns, and ");
			else if (tempstat > 0.7)
				aurastring.addElement("It almost glows with dark, hateful intentions, and ");
			else
				aurastring.addElement("It is surrounded by a black, violently shifting stain that flows out from deep inside, and ");
		}
		else aurastring.addElement("It is perfectly clear, and ");

		tempstat = targetp.getFloat("asshole");

		if (tempstat > 0)
		{
			if (tempstat < 0.3)
				aurastring.addElement("has a unpleasant air to it.");
			else if (tempstat < 0.6)
				aurastring.addElement("exudes an unpleasant, almost palpable haze. ");
			else
				aurastring.addElement("is extremely unpleasant in some way you can't quite put your finger on... almost revolting to look upon.");
		}
		else 
			aurastring.addElement("smoothly shaded.");

		p.hears(aurastring);

		return true;
	}

	public static final String[] readAuraFailure =
	{
		"You stare intently for a few moments, but see nothing special.",
		"You squint inneffectually for a few seconds, unable to gain any insight.",
		"You look long and hard, but nothing unusual comes to mind."
	};
	
	public static final String[] auraPassVerb =
	{
		" stares", " looks", " glances", " looks"
	};

	public static final String[] auraFailureVerb =
	{
		" stares", " looks", " squints", " blinks a few times, and looks", " blinks and stares"
	};

}

/*
  "You stare deep into the soul of "+tempthing.the()+tempthing.name()+", but find it disappointingly empty.");

  Check skill

  Print external

  Check aura string

  Produce Psyche Aura Description
*/
