package twisted.reality.author;

import twisted.reality.*;

/**
 * This verb allows you to describe an object.  It will prompt you for
 * a longer description in an editing window, so don't enter it on the
 * commandline. :)<br>
 *
 * Usage: <code>&gt; describe <b>&lt;objectname&gt;</b>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Describe extends Verb
{
	public Describe()
	{
		super("describe");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		d.subject().hears("Please enter a description for the " + d.directObject().name());
		d.subject().requestResponse
			(
			 new DescribeProcessor(d.directObject(),d.subject()),"Description of "
			 + d.directObject().name() + ".",d.directObject().DESC()
			 );
		return true;
	}
}
