package twisted.reality;

import java.io.IOException;
import java.io.StreamTokenizer;

import twisted.util.SetupWrapper;

import java.util.Vector;

/**
 * An exact clone of ThingFactory, except it returns a Location. (and
 * handles the "open", "opaque", and "shut" bits).
 *
 * @version 1.0.0, 1 Jul 1999
 * @author Glyph Lefkowitz
 */

class LocationFactory extends ThingFactory
{
	LocationFactory(StreamTokenizer a, SetupWrapper b)
	{
		super(a,b);
	}
	
	protected boolean handleIt(String tok) throws RPException, IOException
	{
		/* 'open' for backward compatibility only */
		if((tok == "open") || (tok == "broadcast"))
		{
			((Location) thi).setBroadcast(true);
			return true;
		}
		if (tok == "opaque")
		{
			((Location) thi).setContentsVisible(false);
			return true;
		}
		if (tok == "shut")
		{
			((Location) thi).setContentsOperable(false);
			return true;
		}
		return super.handleIt(tok);
	}
	
	public Thing generatedClass()
	{
		return new Location();
	}
}
