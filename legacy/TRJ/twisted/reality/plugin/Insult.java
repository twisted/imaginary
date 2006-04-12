package twisted.reality.plugin;

import twisted.reality.Verb;
import twisted.reality.Sentence;
import twisted.reality.RPException;

/**
 * This is the simplest verb it is possible to write.  It's intended
 * as a primer. Please don't run this in the game, it's disappointing
 * :)
 * <br>
 *
 * Usage: <code>&gt; insult</code>
 * @version 1.0.0, 15 Jun 1998
 * @author Glyph Lefkowitz
 */

public class Insult extends Verb
{
	/**
	 * Source code:
	 * <pre>
	 * public Insult()
	 * {
	 * 	super("insult");
	 * }
	 * </pre> 
	 * <br>
	 * 
	 * This names the verb 'insult'.
	 */
	public Insult()
	{
		super("insult");
	}
	/**
	 * Source code:
	 * <pre>
	 * public boolean action(Sentence d) throws RPException
	 * {
	 * 	d.subject().hears("You bastard!!!");
	 * 	return true;
	 * }
	 * </pre>
	 * <br>
	 * 
	 * This just displays "You bastard!!!" to the player who typed 'insult'.
	 * The verb succeeded, so it returns true.
	 */
	public boolean action(Sentence d) throws RPException
	{
		d.subject().hears("You bastard!!!");
		return true;
	}
}
