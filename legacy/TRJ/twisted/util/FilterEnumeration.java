package twisted.util;

import java.util.*;

public abstract class FilterEnumeration implements Enumeration
{
	Enumeration internal;
	Object temp;
	
	public FilterEnumeration (Enumeration e)
	{
		internal=e;
	}
	
	public boolean hasMoreElements()
	{
		if (temp != null) return true;
		Object o;
		while(internal.hasMoreElements())
		{
			o=internal.nextElement();
			if(filter(o))
			{
				temp=o;
				return true;
			}
		}
		return false;
	}
	
	public Object nextElement()
	{
		if (temp==null) hasMoreElements();
		Object tp=temp;
		temp=null;
		return tp;
	}
	
	public abstract boolean filter(Object o);
}
