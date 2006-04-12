package divunal.common.vehicles.guymelf;

import twisted.reality.*;

/**
 * Makes you go somewhere.
 *
 * Usage: <code>&gt; go <b>&lt;direction&gt;</b></code>
 *
 * @version 1.0.0, 15 Jun 1998
 * @author Glyph Lefkowitz
 */

public class GuymelfGo extends Verb
{
	public GuymelfGo()
	{
		super("go");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (d.subject().place() == d.verbObject())
		{
			Portal x = ((Room) d.subject().place()).getPortal(d.directString());
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
