package twisted.reality.author;

import twisted.reality.*;

/**
 * This verb adds a feature to an existing object.<br>
 *
 * Usage: <code>&gt; enable <b>"&lt;object name&gt;"</b> to
 * <b>&lt;java classname of verb&gt;</b></code><br> OR: <code>&gt;
 * disable <b>"&lt;object name&gt;"</b> from <b>&lt;java classname of
 * verb&gt;</b></code><br>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Enable extends Verb
{
	public Enable()
	{
		super("enable");
		alias("disable");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		try
		{

			Thing t = d.directObject();
			if(d.verbString().equals("disable"))
			{
				t.removeVerb(d.indirectString("from") );
				d.subject().hears("Disabled.");
			}
			else
			{
				// if removeVerb blows up because the verb wasn't on
				// the object to begin with.
				t.addVerb(d.indirectString("to"));
				d.subject().hears("Enabled.");
			}
		}
		catch (ClassNotFoundException e)
		{
			// If removeVerb blows up because the verb class wasn't
			// found.
			d.subject().hears(d.verbString()+" failed : " + e);
		}
		catch (IllegalArgumentException iae)
		{
			// if removeVerb blows up because synonyms for this verb
			// overlap with a verb already enabled on it.
			d.subject().hears(iae.getMessage());
		}
		return true;
	}
}
