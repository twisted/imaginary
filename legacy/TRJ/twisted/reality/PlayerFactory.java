package twisted.reality;

import java.io.IOException;
import java.io.StreamTokenizer;

import twisted.util.SetupWrapper;

/**
 * This is the same as ThingFactory, but it creates players (as the
 * name implies).
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class PlayerFactory extends LocationFactory
{
	public PlayerFactory(StreamTokenizer a,SetupWrapper b)
	{
		super(a,b);
	}
	protected boolean handleIt(String tok) throws RPException, IOException
	{
		if(tok == "ability")
		{
			zq.nextToken();
			Age.log("Ability: " + zq.sval,Age.VERBOSE);
			try
			{
				((Player) thi).addAbility(zq.sval);
			} catch (Exception e) {
				Age.log("Error adding ability to "+thi.name()+": "+e);
			}
			return true;
		}
		else if(tok == "architect")
		{
			((Player) thi).godBit = true;
			return true;
		}
		else if(tok == "passwd")
		{
			zq.nextToken();
			((Player) thi).password = zq.sval;
			return true;
		}
		else if(tok == "password")
		{
			zq.nextToken();
			((Player) thi).password = twisted.util.UnixCrypt.crypt(zq.sval,thi.NAME());
			return true;
		}
		
		return super.handleIt(tok);
	}
	
	public Thing generatedClass()
	{
		return new Player();
	}
}
