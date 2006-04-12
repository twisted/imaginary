package demo;

import twisted.reality.*;

/**
 * Makes the guymelf you are piloting go somewhere.
 *
 * Usage: <code>&gt; go <b>&lt;direction&gt;</b></code>
 *
 */

public class GuymelefGo extends Verb
{
	public GuymelefGo()
	{
		super("go");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (d.subject().place() == d.verbObject())
		{
			Portal x = ((Room) d.subject().place().place()).getPortal(d.directString());
			if(x != null)
			{
				x.propels(d.verbObject());
			}
			else
			{
				d.subject().hears("You can't go that way.");
			}

			return true;

		}

		return false;
	}
}
