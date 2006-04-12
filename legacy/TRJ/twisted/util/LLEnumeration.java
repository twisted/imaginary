package twisted.util;

import java.util.Enumeration;

class LLEnumeration implements Enumeration
{
	Linker l;
	boolean keyz;
	LLEnumeration(Linker a)
	{
		l=a;
		keyz=false;
	}
	
	LLEnumeration(Linker a, int b)
	{
		l=a;
		keyz=true;
	}
	
	public Object nextElement()
	{
		if(hasMoreElements())
		{
			Linker m=l;
			l=l.next;
			
			return keyz ? m.key : m.val;
		}
		return null;
	}
	
	public boolean hasMoreElements()
	{
		return (l!=null);
	}
}
