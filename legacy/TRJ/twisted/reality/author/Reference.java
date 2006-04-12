package twisted.reality.author;

import twisted.reality.*;

/**
 * Add an alias to a thing - IE, make it callable by some name other
 * than its own.  An example of this is the Reality Pencil, which is
 * referenced to simply 'pencil'. <br>
 *
 * Usage: <code>&gt; reference <b>&lt;thing&gt;</b> to <b>&lt;new
 * name&gt;</b></code> OR: <code>&gt;
 * unreference <b>"&lt;thing&gt;"</b> from <b>&lt;old alias&gt;</b></code><br>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Reference extends Verb
{
	public Reference()
	{
		super("reference");
		alias("unreference");
		setDefaultPrep("with");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing t = d.directObject();
		String s = d.indirectString("to");
		String m;
		
		if(d.verbString().equals("reference"))
		{
			t.addSyn(s);
			
			m = " can now be referenced as ";
		}
		else
		{
			t.removeSyn(s);

			m = " can no longer be referenced as ";
		}
		d.subject().hears(t.name() + m + s + ".");
		return true;
	}
}
