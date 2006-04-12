package divunal.common.skills;

import twisted.reality.*;
import java.util.Enumeration;
import java.util.Vector;
import divunal.common.Skill;
import divunal.Divunal;

/**
 * A skill which allows players to look at someone else covertly.
 * It is based on Dex (sneakiness) and opposed by Psyche (perception)
 *
 * Usage: <code>&gt; glance at <b>&lt;thing&gt;</b></code>
 * Usage: <code>&gt; glance <b>&lt;thing&gt;</b></code>
 *
 * @version 1.0.0, 14 Sep 1999
 * @author Tenth
 */

public class Glance extends Skill
{
	public Glance()
    {
		super("glance");
    }

	public float dailyIncrement() {return 0.05f;}
	public float initialValue() {return 0.2f;}
	public String relevantStat() {return "dexterity";}
	public String skillName() {return "glance";}

	public boolean action(Sentence d) throws RPException
	{
		/*
		  If it's a player, let them know if the glancer has failed.
		  If it's an object, it always works.
		 */

		Player p = d.subject();
		Thing foo=null;
		
		if(d.hasIndirect("at"))
		{
			try
			{
				foo=d.indirectObject("at");
			}
			catch (NotInterestingException nie)
			{
				p.hears("There is nothing special about the "+d.indirectString("at") +".");
			}
		}
		else if (d.hasDirect())
		{
			try
			{
				foo=d.directObject();
			}
			catch(NotInterestingException nie)
			{
				Object[] nspabt = {"There is nothing special about the ",d.directString(),"."};
				p.hears(nspabt);
			}
		}
		else 
		{
			p.hears("You'll have to be a bit more specific than that.");
		}

		if (foo != null)
		{
			if (foo instanceof Player)
			{
				Player targetplayer = (Player) foo;
				if (targetplayer == p)
				{
					p.hears("You glance down furtively at yourself, hoping that you won't notice... But, alas, you do. Perhaps you should find someone else to spy on.");
				}
				else
				{
					// The player's Dex and practice at glancing versus the target's psyche. Glancing is pretty easy to do for the most part.
					float result = (
									getCurrentSkill(p) +
									Divunal.dexterity(p)+
									Divunal.makeModifier()
									) - Divunal.psyche(targetplayer);
					if (result < 0)
					{
						Object[] tnotice = {p," glances at you."};
						targetplayer.hears(tnotice);
					}
					if (result < -0.3)
					{
						Object[] pNoticeNoticed = {"You glance at ",targetplayer," out of the corner of your eye, but ",Pronoun.of(targetplayer)," seems to notice anyway."};
						p.hears(pNoticeNoticed);
					}
				}
			}
			else
			{
				Object[] pGlanceObject = {"You glance furtively at ",foo,", hoping that ",Pronoun.of(foo)," doesn't notice your wandering eyes."};
				p.hears(pGlanceObject);
			}
		}
		else
		{
			p.hears("You glance furtively at... the... What are you glancing at, again?");
			return true;
		}

		p.setFocus(foo);
		return true;
	}
}
