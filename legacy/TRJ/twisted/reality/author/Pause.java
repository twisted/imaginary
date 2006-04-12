package twisted.reality.author;

import twisted.reality.*;

/**
 * Pauses a player for 10 seconds.
 */

public class Pause extends Verb
{
	public Pause()
	{
		super("pause");
	}
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing psr = d.directObject();
		if (psr instanceof Player)
		{
			Player p = (Player) psr;
			p.delay(100);
			d.subject().hears("Delayed.");
		}
		else
		{
			d.subject().hears("You can't delay a non-player.");  
		}
		return true;
	}
}
