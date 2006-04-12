package twisted.util;

import java.util.*;

public class KeyFilterEnumeration implements Enumeration
{
	Enumeration internalK;
	Enumeration internalV;
	Object temp;
	
	public KeyFilterEnumeration (Enumeration k,Enumeration v)
	{
		internalK=k;
		internalV=v;
	}
	
	public boolean hasMoreElements()
	{
		if (temp != null) return true;
		Object o,p;
		while(internalK.hasMoreElements())
		{
			o=internalK.nextElement();
			p=internalV.nextElement();
			if(filterKey(o) && filterVal(p))
			{
				temp=p;
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
	
	public boolean filterKey(Object o)
	{
		return true;
	}
	public boolean filterVal(Object o)
	{
		return true;
	}

}
