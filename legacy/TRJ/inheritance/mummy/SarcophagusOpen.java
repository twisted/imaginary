package inheritance.mummy;

import twisted.reality.*;

/**
 * When you play the flute, the sarcophagus opens.  This is the code
 * that does that.
 */

public class SarcophagusOpen extends Verb
{
	public SarcophagusOpen()
	{
		super("play");
	}

	public boolean action(Sentence d)
	{
		
		return true;
	}
}
