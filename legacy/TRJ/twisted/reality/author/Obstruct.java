package twisted.reality.author;

import twisted.reality.*;

/**
 * This is to obstruct an exit with a door.  See divunal world
 * development info for more.
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Obstruct extends Verb
{
	public Obstruct ()
	{
		super ("obstruct");
		alias ("unobstruct");
		setDefaultPrep ("with");
	}
	public boolean action (Sentence d) throws RPException
	{
		if(!d.subject().isGod())
		{
			return false;
		}
		Player p = d.subject();
		Thing door = d.withObject();
		String direction = d.directString();
		Room dplace = (Room) d.place();
		Portal target = dplace.getPortal(direction);
		
		if (target != null)
		{
			door.place (dplace);
			target.setThing(door);
			Portal back = target.backtrack();
			if (back != null)
			{
				back.setThing(door);
			}

			Object[] godhears = {"You obstruct the " + direction + " exit with ",door,"."};
			Object[] otherhears = {p," sets ",door," into place across the ",direction," exit, and it melds into a perfect fit."};
			d.place().tellAll(p, godhears, otherhears);
		}
		else
		{
			p.hears("There is no " + direction + " exit, making it rather difficult to obstruct.");
		}
		return true;
	}
	
}
