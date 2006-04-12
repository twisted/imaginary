package twisted.reality.author;

import twisted.reality.*;

/**
 * <b>mood [local-thing : foo] to [string : mood]</b>
 * 
 * <p>Sets the mood of <i>foo</i> to <i>mood</i>.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class MoodSet extends Verb
{
	public MoodSet()
	{
		super("mood");
		alias("unmood");
		setDefaultPrep("with");
	}
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;

		if (d.verbString().equals("mood"))
		{
			String moodstring = d.indirectString("to");
			if(moodstring.equals("null"))
				moodstring = null;
			d.directObject().mood(moodstring);
			d.subject().hears("Mood set.");
		}
		else
		{
			d.directObject().mood(null);
			d.subject().hears("Mood removed.");
		}
		return true;
	}
}
