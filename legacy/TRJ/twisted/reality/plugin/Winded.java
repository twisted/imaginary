package twisted.reality.plugin;

import twisted.reality.*;
/**
 * If you enable this * verb on a Player, they will hear a sarcastic
 * message whenever they try to use ANY verb. A simple example of how
 * to override verbs... Although it should be pointed out that this
 * verb should only be enabled on someone temporarily.
 * 
 * @author Glyph */

public class Winded extends Verb
{
	public Winded()
	{
		super("*");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		d.subject().hears("I'm sure you'd love to `"+d.fullString()+"', but you're just too tired.");
		return true;
	}
}
