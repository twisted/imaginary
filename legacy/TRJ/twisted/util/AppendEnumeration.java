package twisted.util;

import java.util.*;

/**
 * This is an enumeration that gloms a whole bunch of other
 * enumerations together.
 * 
 * @version 0.99.1, 15 Jun 1998
 * @author Glyph Lefkowitz
 */

public class AppendEnumeration implements Enumeration
{
	twisted.util.LinkedList enumerations;
	
	public AppendEnumeration()
	{
		enumerations=new twisted.util.LinkedList();
	}
	
	public void add(Enumeration e)
	{
		enumerations.put(e,e);
	}
	
	public void append(Object o)
	{
		if (o instanceof Enumeration)
		{
			add((Enumeration)o);
		}
		else
		{
			add(new SingleEnumeration(o));
		}
	}
	
	public Object nextElement()
	{
		if(all==null) all=enumerations.elements();
		if(all.hasMoreElements())
		{
			while((current==null || !current.hasMoreElements()) && all.hasMoreElements())
			{
				current=(Enumeration) (all.nextElement());
			}
			if(current.hasMoreElements())
			{
				return current.nextElement();
			}
			return null;
		}
		else
		{
			if(current != null) 
			{
				return current.nextElement();
			}
		}
		return null;
	}
	
	public boolean hasMoreElements()
	{
		if(all==null) all=enumerations.elements();
		if(all.hasMoreElements())
		{
			while((current==null || !current.hasMoreElements()) && all.hasMoreElements())
			{
				current=(Enumeration) (all.nextElement());
			}
			return current.hasMoreElements();
		}
		else
		{
			if(current != null) return current.hasMoreElements();
		}
		return false;
	}
	
	public static void main(String[] args)
	{
		// a simple test to see if it works before foisting it upon the world
		Hashtable h=new Hashtable();
		twisted.util.LinkedList l=new twisted.util.LinkedList();
		AppendEnumeration e=new AppendEnumeration();
		h.put ("EVIL","EVIL");
		h.put ("This is a test.","Isn't it?");
		h.put ("OK, enough testing. It should work now.", "Shouldn't it?");
		l.put ("So, H worked. Now what about some other weird kind of enumeration?","Naah.");
		l.put ("testing. Testing.","one two.");
		l.put ("EVIL","EVIL");
		e.add(h.elements());
		e.add(l.elements());
		e.add(h.elements());
		e.add(l.elements());
		while(e.hasMoreElements())
		{
			System.out.println(e.nextElement());
		}
	}
	
	public Enumeration current;
	public Enumeration all;
}
