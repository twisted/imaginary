package twisted.util;
import java.util.Enumeration;

/**
 *  This is getting reeely silly, bit these gazillions of enumerations
 *  are actually probably pretty good for creating test conditions.
 */

public class SingleEnumeration implements Enumeration
{
	Object mVal;
	public SingleEnumeration (Object o)
	{
		mVal=o;
	}
	public boolean hasMoreElements()
	{
		return (mVal!=null);
	}
	public Object nextElement()
	{
		Object tmp;
		tmp=mVal;
		mVal=null;
		return tmp;
	}
}
