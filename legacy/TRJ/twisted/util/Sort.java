package twisted.util;

import java.util.Vector;
import java.util.Enumeration;

public class Sort
{
	public interface Comparator
	{
		int SAME_AS=0;
		int GREATER_THAN=1;
		int LESS_THAN=-1;
		
		int compare(Object a, Object b);
	}
	
	static class Alpha implements Comparator
	{
		public int compare(Object a, Object b)
		{
			String x = String.valueOf(a);
			String y = String.valueOf(b);
			
			/* ALPHAbetical, not ASCIIbetical */
			
			x = x.toLowerCase();
			y = y.toLowerCase();
			
			int nearcomp = x.compareTo(y);
			
			if (nearcomp > 0)
				return GREATER_THAN;
			else if (nearcomp < 0)
				return LESS_THAN;
			else
				return SAME_AS;
		}
	}
	
	public static Comparator ALPHABETICAL=new Alpha();
	
	public static Vector quick(Vector v, Comparator c)
	{
		Vector lessThan = new Vector(v.size()/2);
		Vector greaterThan = new Vector(v.size()/2);
		if(v.size() <= 1)
			return v;
		Object pivot = v.elementAt(0);

		for(int i = 1; i < v.size(); i++)
		{
			Object item = v.elementAt(i);
			int comparison = c.compare(item,pivot);
			if( comparison > Comparator.LESS_THAN )
				greaterThan.addElement(item);
			else
				lessThan.addElement(item);
		}
		lessThan = quick(lessThan,c);
		greaterThan = quick(greaterThan,c);
		lessThan.addElement(pivot);
		for(int i = 0; i < greaterThan.size(); i++)
			lessThan.addElement(greaterThan.elementAt(i));
		return lessThan;
	}
	
	public static void main(String[] args)
	{
		Vector v = new Vector();
		v.addElement("alpha");
		v.addElement("ALPHA");
		v.addElement("gamma");
		v.addElement("zed");
		v.addElement("zZeEdDDd");
		v.addElement("foo");
		v.addElement("bar");
		v.addElement("baz");
		v.addElement("quux");
		v.addElement("whee");
		
		v=quick(v,ALPHABETICAL);
		
		Enumeration e = v.elements();
		while (e.hasMoreElements())
		{
			System.out.println(e.nextElement());
		}
	}
}
