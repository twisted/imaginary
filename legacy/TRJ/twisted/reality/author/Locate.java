package twisted.reality.author;

import twisted.reality.*;

/**
 * This verb, based upon the popular Linux command, locates an object
 * somewhere in the game.<br>
 *
 * Usage: <code>&gt; locate <b>&lt;thing to search for&gt;</b></code>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Locate extends Verb
{
	public Locate()
	{
		super("locate");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing t = Age.theUniverse().findThing(d.directString());
		Object[] subjhr;
		if(t!=null)
		{
			if(t.place()!=null)
			{
				if(t.place() instanceof Player)
				{
					Object[] tmpa = {t.place().NAME()," is holding ",t,"."};
					subjhr=tmpa;
				}
				else
				{
					Object[] tmpb = {t," is in ",t.place(),"."};
					subjhr=tmpb;
				}
			}
			else
			{
				Object[] tmpc = {"You quest after ",t," but you can't seem to place ",Pronoun.obj(t),"."};
				subjhr=tmpc;
			}
		}
		else
		{
			Object[] tmpd = {"You can't seem to conceive of such a thing."};
			subjhr=tmpd;
		}

		Object[] otherhear = {d.subject(), " looks distant for a moment."};

		d.place().tellAll(d.subject(), subjhr, otherhear);
		
		return true;
	}
}
