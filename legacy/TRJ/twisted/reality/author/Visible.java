package twisted.reality.author;

import twisted.reality.*;

/**
 * This verb can set the Visible bit of an object. Do this to
 * containers to allow or prevent their contents from being seen
 * or looked at. (see Visible for blocking other forms of interaction)
 *
 * Usage: <code>&gt; vis <b>&lt;thing&gt;</b></code> <br>
 *        <code>&gt; devis <b>&lt;thing&gt;</b></code> <br>
 *
 * @version 1.0.0, 19 Aug 1999
 * @author David Sturkowitz
 */

public class Visible extends Verb
{
	public Visible()
	{
		super("vis");
		alias("devis");
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

		if (v.equals("vis"))
		{
			Object[] pVis = {"The contents of ",t," are now visible."};
			t.setContentsVisible(true);
			p.hears(pVis);
		}
		else
		{
			Object[] dVis = {"The contents of ",t," are no longer visible."};
			t.setContentsVisible(false);
			p.hears(dVis);
		}
		return true;
	}
}
