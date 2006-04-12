package twisted.reality.plugin;

import twisted.reality.*;

/**
 * This verb for putting stuff into containers.
 * 
 * @author Bento
 */

public class Put extends Verb
{
	public Put()
	{
		super("put");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player plr = d.subject();
		if (d.hasDirectObject())
		{
			Thing t = d.directObject();
			Location c = (Location)d.verbObject();
			String verbPrep = c.getString("preposition");
			if (verbPrep == null)
				verbPrep = "in";
			if(!verbPrep.equals(d.verbPreposition()))
				// (if it's the direct object, or the room, or
				// something ... more complex tests can be added
				// later.)
				return false;
			
			if(t.place()==plr)
			{
				if (c instanceof Location)
				{
					if (c.areContentsOperable())
					{
						if (t==c)
						{
							plr.hears("That would be silly.");
							return true;
						}
						Object[] putsin = {plr, " puts ",t," ",verbPrep," ",c,"."};
						if(t.moveTo(c,putsin))
						{
							Object[] mlsti = {"You put ",t," ",verbPrep," ",c,"."};
							plr.hears(mlsti);
						}
						else
						{
							throw new NoSuchVerbException("put");
						}
					}
					else
					{
						Object[] closed = {"You can't put anything ",verbPrep," ",c,"... It's closed."};
						plr.hears(closed);
					}
				}
				else 
				{
					Object[] asdf = {"You can't put things ",verbPrep," ",c,"."};
					plr.hears(asdf);
				}	 
			} 
			else
			{
				Object[] hjkl = {"You aren't holding ",t,"."};
				plr.hears(hjkl);
			}
			return true;
		}
		else
		{
			plr.hears("You don't have one of those.");	
		}
		return true;
	}
}
