package twisted.util;
import java.util.Enumeration;

/**
 * A class for reproducing an enumeration many times
 */

public class EnumerationFactory
{
	public Enumeration elements()
	{
		return new SimpleEnumerate(start);
	}
	class SimpleEnumerate implements Enumeration
	{
		SimpleEnumerate(SimpleLink s)
		{
			marker=s;
		}
		SimpleLink marker;
		public Object nextElement()
		{
			SimpleLink tmp=marker;
			marker=marker.next;
			return tmp.val;
		}
		public boolean hasMoreElements()
		{
			return (marker!=null);
		}
	}
	class SimpleLink
	{
		Object val;
		SimpleLink next;
	}
	SimpleLink start;
	
	public EnumerationFactory(Enumeration e)
	{
		SimpleLink end;
		start=end=new SimpleLink();
		while (e.hasMoreElements())
		{
			end.val=e.nextElement();
			if (e.hasMoreElements())
			{
				end.next=new SimpleLink();
				end=end.next;
			}
		}
		end.next=null;
		if (start.val==null)
		{
			start=null;
		}
	}
}
