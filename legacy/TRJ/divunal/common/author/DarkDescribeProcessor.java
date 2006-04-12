package divunal.common.author;

import twisted.reality.*;

public class DarkDescribeProcessor implements ResponseProcessor
{
	public DarkDescribeProcessor(Thing a,Player p)
	{
		th=a;
		pl=p;
	}
	
	public void gotResponse(String s)
	{
		th.putString("darkDescription",s);
		pl.hears("Dark description changed.");
	}
	
	Player pl;
	Thing th;
}
