package gloop;

import java.lang.reflect.*;

import java.util.Vector;
import java.util.Enumeration;

public class BolgMethod implements Bolg
{
	Object meth;
	BolgObject bound;
	BolgMethod(BolgObject toBind, Object methodOrVector)
	{
		bound=toBind;
		meth=methodOrVector;
	}

	public void set(String key,Object value) throws NoSuchFieldException
	{
		throw new NoSuchFieldException(key);
	}
	
	public Object get(String key) throws NoSuchFieldException
	{
		throw new NoSuchFieldException(key);
	}

	public Object call(Object[] args)
		throws IllegalArgumentException,
		IllegalAccessException,
		InvocationTargetException
	{
		if (meth instanceof Method)
		{
			Method tech = (Method) meth;
			return tech.invoke(bound.wrapped, args);
		}
		else// if (meth instanceof Vector)
		{
			Enumeration ejb = ((Vector)meth).elements();
			while(ejb.hasMoreElements())
			{
				Method mark = (Method) ejb.nextElement();
				try
				{
					return mark.invoke(bound.wrapped,args);
				}
				catch(IllegalArgumentException iae){}
				catch(IllegalAccessException iaee){}
			}
			throw new IllegalArgumentException(String.valueOf(args));
		}
	}
	public int hashCode()
	{
		return meth.hashCode();
	}
}
