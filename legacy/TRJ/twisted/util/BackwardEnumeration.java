package twisted.util;
import java.util.Enumeration;

public class BackwardEnumeration implements Enumeration
{
	Enumeration e;
	public BackwardEnumeration(Enumeration se)
	{
		Stack s=new Stack();
		
		while(se.hasMoreElements())
		{
			s.push(se.nextElement());
		}
		e=s.elements();
	}
	
	public Object nextElement()
	{
		return e.nextElement();
	}
	public boolean hasMoreElements()
	{
		return e.hasMoreElements();
	}
}
