package twisted.reality.author;

import twisted.reality.*;

/**
 * This verb will set the component bit of an object. Do this to
 * things like fixtures, walls, and doors.  Any object which is a
 * distinct object but also an integral part of its container is a
 * component.<br>
 *
 * Usage: <code>&gt; nail <b>&lt;thing&gt;</b></code>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Nail extends Verb
{
	public Nail()
	{
		super("nail");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing t = d.directObject();
		t.setComponent(true);
		d.subject().hears("Wham.");
		return true;
	}
}
