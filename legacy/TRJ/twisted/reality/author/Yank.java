package twisted.reality.author;

import twisted.reality.*;

/**
 * This verb will UNset the component bit of an object. Do this to
 * things like people and cats which you have accidentally 'nail'ed.
 * <br>
 *
 * Usage: <code>&gt; yank <b>&lt;thing&gt;</b></code> <br>
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Yank extends Verb
{
	public Yank()
	{
		super("yank");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing t = d.directObject();
		t.setComponent(false);
		d.subject().hears("Slurp.");
		return true;
	}
}
