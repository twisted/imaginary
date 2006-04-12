package twisted.reality.plugin;

import twisted.reality.*;

/**
 * Makes you go through the specified exit.
 *
 * The Faucet normally has one letter shortcuts for "go (direction)",
 * namely n, s, e, w, ne, se, nw, sw, u, and d, which correspond to
 * the directions you'd probably expect.
 *
 * Usage: <code>&gt; go <b>&lt;direction&gt;</b></code>
 *
 * @version 1.0.0, 15 Jun 1998
 * @author Glyph Lefkowitz */

public class Go extends Verb
{
	public Go()
	{
		super("go");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (d.subject().place() instanceof Room)
		{
			Portal x = ((Room) d.subject().place()).getPortal(d.directString());
			if(x != null)
			{
				x.propels(d.subject());
			}
			else
			{
				d.subject().hears("You can't go that way.");
			}
		}
		else
		{
			d.subject().hears("You can't go any way.");
		}
		return true;
	}
}
