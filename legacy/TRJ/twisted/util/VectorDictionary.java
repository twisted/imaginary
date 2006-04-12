package twisted.util;

import java.util.Dictionary;
import java.util.Vector;
import java.util.Enumeration;

/**
 * When JDK 1.2 stabilizes (I.E. there is a functional port for more
 * than 2 platforms), this will be incorporated into the Collections
 * framework.
 **/

public class VectorDictionary extends Dictionary
{
	static class ArrayVector extends Vector
	{
		public ArrayVector(Object[] arrayvect)
		{
			elementData=arrayvect;
			elementCount=arrayvect.length;
		}
	}
	
	Vector var;
	
	public VectorDictionary()
	{
		this(new Vector());
	}
	
	public VectorDictionary(Vector v)
	{
		var=v;
		if (var==null)
		{
			var=new Vector();
		}
		if (var.size()%2!=0)
		{
			throw new IllegalArgumentException("Vector must have an even number of components to be a valid dictionary.");
		}
	}
	
	public VectorDictionary(Object[] initr)
	{
		this(new ArrayVector(initr));
	}
	
	public int size()
	{
		return var.size()/2;
	}
	
	public boolean isEmpty()
	{
		return (size()==0);
	}
	
	public Object get(Object key)
	{
		for (int i = 0; i<var.size(); i+=2)
		{
			//System.out.println("TEST A: "+var.elementAt(i)+"\tTEST B: "+key);
			if (var.elementAt(i).equals(key))
			{
				return var.elementAt(i+1);
			}
		}
		return null;
	}
	
	public Object remove(Object key)
	{
		for (int i = 0; i<var.size(); i++)
		{
			if (var.elementAt(i).equals(key))
			{
				var.removeElementAt(i);
				Object o = var.elementAt(i);
				var.removeElementAt(i);
				return o;
			}
		}
		return null;
	}
	
	public Object put(Object key, Object val)
	{
		for (int i = 0; i<var.size(); i++)
		{
			if (var.elementAt(i).equals(key))
			{
				Object tmp = var.elementAt(i+1);
				/* and next week, on 'coding with the smurfs'...
				   var.setElementAt(val,i); */
				var.setElementAt(val,i+1);
				return tmp;
			}
		}
		var.addElement(key);
		var.addElement(val);
		return null;
	}
	
	public Enumeration elements()
	{
		return new SkipEnumeration(var.elements(),true);
	}
	
	public Enumeration keys()
	{
		return new SkipEnumeration(var.elements(),false);
	}
	
	public class SkipEnumeration implements Enumeration
	{
		Enumeration e;
		public SkipEnumeration (Enumeration inE, boolean skipFirst)
		{
			e=inE;
			if (skipFirst)
			{
				if (e.hasMoreElements())
					e.nextElement();
			}
		}
		public boolean hasMoreElements()
		{
			return e.hasMoreElements();
		}
		public Object nextElement()
		{
			if (!e.hasMoreElements()) return null;
			
			Object ret = e.nextElement();
			if (e.hasMoreElements())e.nextElement();
			return ret;
		}
	}
	
	public static Object[] twiddle(Object[] x)
	{
		Object[] y = new Object[x.length];
		for (int i = 0; i < x.length; i+=2)
		{
			int z = i+1;
			y[i]=x[z];
			y[z]=x[i];
		}
		return y;
	}
}
