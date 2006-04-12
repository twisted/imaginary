
package twisted.reality.plugin;

import twisted.reality.*;

/**
 * This verb allows you to quit the game via a command rather than by
 * closing the Faucet.  ;-)
 * 
 * @author Probably Glyph */

public class Quit extends Verb
{
	public Quit()
	{
		super("quit");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Age.theUniverse().disconnect(d.subject());
		return true;
	}
}
