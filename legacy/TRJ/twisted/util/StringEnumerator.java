package twisted.util;

import java.util.Enumeration;

public class StringEnumerator implements Enumeration
{
	public StringEnumerator(String mstr)
	{
		s=mstr;
		count=0;
	}
	int count;
	public boolean hasMoreElements()
	{
		if(s==null) return false;
		return ( count < s.length() );
	}
	public char nextChar()
	{
		return s.charAt(count++);
	}
	public Object nextElement()
	{
		char[] c = {s.charAt(count++)};
		return new String(c);
	}
	String s;
}
