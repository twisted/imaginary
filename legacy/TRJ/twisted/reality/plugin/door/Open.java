package twisted.reality.plugin.door;

import twisted.reality.*;

/**
 * The "open" verb for the nifty Jedin Style Doors(TM). See Door.java
 * for more information on these wonderful things.
 * 
 * @author Jedin */

public class Open extends Verb
{
	public Open()
	{
		super ("open");
	}
	
	public boolean action(Sentence d) throws RPException
	{

		Thing door = d.directObject();
		Portal way = ((Room)d.place()).getPortalByThing(door);

		
		if (way.isObvious() == false)
		{
			if (door.getBool("locked") == false)
					Door.open(door, d.subject(), d.place());
			else
			{
				Object[] msg = {Name.Of(door), " appears to be locked."};
				d.subject().hears(msg);			
			}
		}
		
		else
		{
			Object[] msg = {Name.Of(door), " is already open."};
			d.subject().hears(msg);
		}
		return true;
	}
}
