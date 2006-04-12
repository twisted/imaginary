package twisted.reality.author;

import twisted.reality.*;

/**
 * <b>barricade [local-portal : exit]</b>
 * <p>This removes an exit from the room permanently.  Please note that
 * since all Portals are actually one-way exits, this will not destroy
 * the reverse exit.</p>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Barricade extends Verb
{
	public Barricade()
	{
		super("barricade");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		if(d.hasDirect())
		{
			Room r = (Room) d.place();
			if( r.getPortal(d.directString())!=null )
			{
				r.removePortal(d.directString());
				d.subject().hears("You close off the exit " + d.directString() + "ward.");
				r.tellEverybodyBut(d.subject(),d.subject().name() + " gestures, and the " + d.directString() + "ward exit vanishes in a puff of smoke.");
			}
			else
			{
				d.subject().hears("That exit doesn't exist.  Sorry.");
			}
		}
		else d.subject().hears("Please specify a direction to barricade.");
		
		return true;
	}
}
