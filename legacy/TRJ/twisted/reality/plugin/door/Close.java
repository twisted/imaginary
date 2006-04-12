package twisted.reality.plugin.door;

import twisted.reality.*;

/**
 * The "close/shut" verb for the nifty Jedin Style Doors(TM). See
 * Door.java for more information on these wonderful things.
 * 
 * @author Jedin */

public class Close extends Verb
{
	public Close()
	{
		super ("close");
		alias ("shut");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing door = d.directObject();
		Portal way = ((Room)d.place()).getPortalByThing(door);
	 
		if (way.isObvious() == true)
			Door.close(door, d.subject(), d.place());
		else
		{
			Object[] msg = {Name.Of(door), " is already closed."};
			d.subject().hears(msg);
		}

		return true;
	}
}
