package twisted.reality.author;

import twisted.reality.*;

/**
 * Manually collect garbage in the JVM (do this if you think you ought
 * to be using less memory)
 * 
 * @version 1.0.0, 15 Jun 1999
 * @author Glyph Lefkowitz
 */

public class GC extends Verb
{
	public GC()
	{
		super("gc");
	}
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		System.gc();
		d.subject().hears("Ker-plunk.");
		return true;
	}
}
