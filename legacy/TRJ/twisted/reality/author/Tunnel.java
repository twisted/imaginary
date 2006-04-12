package twisted.reality.author;

import twisted.reality.*;

/**
 * This creates a passageway from one room to another, once both rooms
 * already exist. <br>
 *
 * Usage: <code>&gt;tunnel <b>&lt;direction&gt;</b> to
 * <b>&lt;destination&gt;</b></code>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Tunnel extends Verb
{
	public Tunnel()
	{
		super("tunnel");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Room mrm = (Room) d.place();
		if(mrm.getPortal(d.directString())==null)
		{
			String toString = d.indirectString("to");
			Thing rm = Age.theUniverse().findThing(toString);
			if (rm != null && rm instanceof Room)
			{
				Room trm = (Room) rm;
				mrm.addPortal(new Portal(mrm,trm,d.directString()));

				
				Object[] godhear = {"An exit opens before you."};
				Object[] obshear = {d.subject()," gestures towards an exit that you don't seem to have noticed before."};
				
				d.place().tellAll(d.subject(),godhear,obshear);
				return true;
			}
			
		}
		/* else */
		{
			Object[] youscrewup = {d.subject(), " gestures towards a wall and looks confused for a moment."};
			Object[] iscrewup = {"You can't tunnel that way!"};
			
			d.place().tellAll(d.subject(),iscrewup,youscrewup);
			return true;
		}
	}
}
