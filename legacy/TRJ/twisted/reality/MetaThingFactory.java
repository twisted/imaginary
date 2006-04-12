package twisted.reality;

import java.io.*;
import twisted.util.*;

/**
 * This is not a feature which will be supported in future versions of
 * Twisted Reality, for reasons too detailed to go into here.  The
 * concept may be useful, however, so we are leaving it in for the
 * time being.
 */

class MetaThingFactory extends ThingFactory
{
	public MetaThingFactory(StreamTokenizer st, SetupWrapper rsw)
	{
		super(st,rsw);
		try
		{
			st.nextToken();
		}
		catch(Exception e) {}
		aaa=st.sval;
	}
	
	public Thing generatedClass()
	{
	
		try
		{
			return ((Thing) Class.forName(aaa).newInstance());
		}
		catch(Exception e)
		{
			
		}
		return null;
	}
	
	String aaa;
}
