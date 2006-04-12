package twisted.reality.author;

import twisted.reality.*;

/**
 * This is what processes the response to the "string" verb.
 *
 * @see twisted.reality.author.StringSet
 * @version 1.0.0, 16 Aug 1999
 * @author David Sturgis
 */

public class StringPropProcessor implements ResponseProcessor
{
	String propkey;
	Object[] tellother;
	public StringPropProcessor(Thing a, Player p, String k, Object[] inTellOther)
	{
		th=a;
		pl=p;
		propkey = k;
		tellother=inTellOther;
	}
	public void gotResponse(String s)
	{
		th.putString(propkey, s);
		Object[] sps={"String Property Set."};
		pl.topPlace().tellAll(pl,sps,tellother);
	}
	
	Player pl;
	Thing th;
}
