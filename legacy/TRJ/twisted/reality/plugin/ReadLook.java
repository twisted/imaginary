package twisted.reality.plugin;

import twisted.reality.*;

/**
 * This verb is for signs, short notes, and other Things with a small
 * ammount of writing on them... Things for which reading or glancing
 * at should have about the same effect. (Basically a glorified alias
 * for "Look" with some feedback.)
 * 
 * @author Tenth */

public class ReadLook extends Verb
{
	public ReadLook()
	{
		super("read");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing foo = null;
		Player p = d.subject();

		try
		{
			foo=d.directObject();
		}
		catch(NotInterestingException nie)
		{
			Object[] nspabt = {"There is nothing special about the ",d.directString(),"."};
			d.subject().hears(nspabt);
		}

		p.setFocus(foo);
		Object[] pHears = {"You read ", foo,"."};
		Object[] fHears = {p, " reads you."};
		Object[] oHears = {p, " reads ", foo,"."};
		d.place().tellAll(p, foo, pHears, fHears, oHears);
		return true;
	}
}
