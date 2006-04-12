package twisted.reality.author;

import twisted.reality.*;

/**
 * This changes the name of an object. <br>
 *
 * Usage: <code>&gt; name <b>&lt;current thing name&gt;</b> to
 * <b>&lt;desired thing name&gt;</b></code>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Name extends Verb
{
	public Name()
	{
		super("name");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		d.directObject().name(d.indirectString("to"));
		return true;
	}
}
