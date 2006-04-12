package twisted.reality.author;

import twisted.reality.*;

/**
 * This verb can set the Operable bit of an object. Do this to
 * containers to allow or prevent their contents from being interacted with,
 * other than by look (see Visible for that)
 *
 * Usage: <code>&gt; op <b>&lt;thing&gt;</b></code> <br>
 *        <code>&gt; deop <b>&lt;thing&gt;</b></code> <br>
 *
 * @version 1.0.0, 19 Aug 1999
 * @author David Sturkowitz
 */

public class Operable extends Verb
{
	public Operable()
	{
		super("op");
		alias("deop");
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
			p.hears("That isn't a location, dumbass.");
			return true;
		}

		String v = d.verbString();

		if (v.equals("op"))
		{
			t.setContentsOperable(true);
			Object[] zoing = {t,"'s contents are now operable."};
			p.hears(zoing);
		}
		else
		{
			t.setContentsOperable(false);
			Object[] zoing = {t,"'s contents are no longer operable."};
			p.hears(zoing);
		}
		return true;
	}
}
