package twisted.reality;

import java.io.IOException;
import java.io.StreamTokenizer;

import twisted.util.SetupWrapper;

import java.util.Vector;

/**
 * This class reads in descriptions of Rooms from files, a-la
 * ThingFactory.
 *
 * @version 1.0.0, 1 Jul 1999
 * @author Glyph Lefkowitz 
 */

class RoomFactory extends LocationFactory
{
	RoomFactory(StreamTokenizer a, SetupWrapper b)
	{
		super (a,b);
	}
	
	protected boolean handleIt(String tok) throws RPException, IOException
	{
		if(tok == "exit")
		{
			
			zq.nextToken();
			String dir = zq.sval;
			
			boolean isob=true;
			
			zq.nextToken();
			String str = zq.sval;
			if (!str.equals("to"))
			{
				isob=false;
			}
			zq.nextToken();
			String rmnm = zq.sval;
			
			String doorthing= null;
			
			if(zq.nextToken() == TT_WORD)
			{
				if (zq.sval.equals("with"))
				{
					zq.nextToken();
					doorthing=zq.sval;
				}else zq.pushBack();
			}
			else zq.pushBack();
			
			
			sw.addSetup(new PortalSetup((Room) thi, rmnm ,dir,doorthing,isob));
			Age.log ( dir +" exit: " + rmnm , Age.EXTREMELY_VERBOSE);
			
			
			return true;
		}
		else if (tok == "claustrophobic")
		{
			((Room) thi).setPortalsVisible(false);
			return true;
		}
		return super.handleIt(tok);
	}
	
	public Thing generatedClass()
	{
		return new Room();
	}
}
