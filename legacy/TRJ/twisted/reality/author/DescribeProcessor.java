package twisted.reality.author;

import twisted.reality.*;

/**
 * This is what processes the response to the "describe" verb.
 *
 * @see twisted.reality.author.Describe
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class DescribeProcessor implements ResponseProcessor
{
	public DescribeProcessor(Thing a,Player p)
	{
		th=a;
		pl=p;
	}
	public void gotResponse(String s)
	{
		th.describe(s);
		pl.hears("Description changed.");
	}
	
	Player pl;
	Thing th;
}
