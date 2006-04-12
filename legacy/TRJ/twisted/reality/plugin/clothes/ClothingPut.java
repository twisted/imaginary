package twisted.reality.plugin.clothes;

import twisted.reality.*;

/**
 * This verb for putting stuff into worn containers; It basically
 * ensures that only the person wearing/carrying the container (if
 * anyone is) can put things in it. Note that we use topPlace() to
 * determine if the container is carried/worn by a Player/Person, if
 * you're doing anything strange with locations.
 *
 * (We might want the regular Put to do something like this
 * eventually...
 *
 * @author Ying & Tenth */

public class ClothingPut extends Verb
{
	public ClothingPut()
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
					if ((c.topPlace() instanceof Player) && (c.topPlace() != plr))
					{
						Object[] notyours = {"You don't have access to ",c,"."};
						plr.hears(notyours);
						return true;
					}

					if (c.areContentsOperable())
					{
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
