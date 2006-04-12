package twisted.reality.author;

import twisted.reality.*;

/**
 * scrutinize [local-thing : thing] 
 *
 * Displays the raw, text format code for thing.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Scrutinize extends Verb
{
	public Scrutinize()
	{
		super("scrutinize");
	}
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing thing = d.directObject();
		Player p = d.subject();
		
		if (p != thing)
		{
			Object[] godhears = {"You stare intently at ",thing,"..."};
			p.hears(godhears);
			
			if (thing instanceof Player)
			{
				Player thingp = (Player) thing;
				if (thingp != p)
				{
					Object[] otherhears = {p," stares at you intently."};
					thingp.hears(otherhears);
				}
			}
		}

		p.requestResponse(rspr,"Internal Structure for "+thing.NAME(),thing.persistance());

		return true;
	}

	ResponseProcessor rspr = new ResponseProcessor(){public void gotResponse(String s){}};
}
