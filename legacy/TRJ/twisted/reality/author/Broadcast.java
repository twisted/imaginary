package twisted.reality.author;

import twisted.reality.*;

/**
 * This verb can set the Broadcast bit of an object. Do this to
 * containers to make their contents listed in the object list.
 *
 * Usage: <code>&gt; broad <b>&lt;thing&gt;</b></code> <br>
 *        <code>&gt; debroad <b>&lt;thing&gt;</b></code> <br>
 *
 * @version 1.0.0, 19 Aug 1999
 * @author David Sturkowitz
 */

public class Broadcast extends Verb
{
	public Broadcast()
	{
		super("broad");
		alias("debroad");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;

		Player p = d.subject();
		Thing subject = d.directObject();
		Location t;

		if (subject instanceof Location)
			t = (Location) subject;
		else
		{
			p.hears("That's not a location, you dumbass.");
			return true;
		}

		String v = d.verbString();

		if (v.equals("broad"))
		{
			t.setBroadcast(true);
			Object[] tb= {t,"'s contents are now broadcast to the room."};
			p.hears(tb);
		}
		else
		{
			t.setBroadcast(false);
			Object[] tb= {t,"'s contents are no longer broadcast to the room."};
			p.hears(tb);
		}
		return true;
	}
}
