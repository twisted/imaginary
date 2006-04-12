package twisted.util;
import java.util.Enumeration;
import java.util.Dictionary;

public class LinkedList extends Dictionary
{
	public static final int KEYS=0;
	public LinkedList()
	{
		ll=null;
		elementCount = 0;
	}
	
	public boolean isEmpty()
	{
		return (ll==null);
	}
	
	public int size()
	{
		return elementCount;
	}
	
	public synchronized Enumeration elements()
	{
		return new LLEnumeration(ll);
	}
	
	public synchronized String toString()
	{
		Enumeration e = elements();
		String s = "[";
		while(e.hasMoreElements())
		{
			if (s != "[")
			{
				s += ", ";
			}
			s += e.nextElement();
		}
		s += "]";
		return s;
	}
	
	public synchronized Enumeration keys()
	{
		return new LLEnumeration(ll,KEYS);
	}
	
	public synchronized Object addElement(Object k)
	{
		/*ll = new Linker(ll,k);
		  elementCount++;*/
		return put(k,k);
	}
	
	public synchronized Object put(Object key, Object value)
	{
		Object qqq;
		qqq=remove(key);
		elementCount++;
		ll = new Linker(ll,key,value);
		return qqq;
	}
	
	public synchronized Object get(Object key)
	{
		if(key==null) return null;
		int opt =key.hashCode();
		Linker l2 = ll;
		Linker l3 = null;
		
		while(l2 != null)
		{
			if(l2.hash == opt)
			{
				if(key.equals(l2.key))
					return l2.val;
			}
			
			l3=l2;
			l2 = l2.next;
		}
		return null;
	}
	
	public synchronized Object remove(Object k)
	{
		int opt = k.hashCode();
		Linker l2 = ll;
		Linker l3 = null;
		
		while(l2 != null)
		{
			if(l2.hash == opt)
			{
				if(k.equals(l2.key))
				{
					Object rvl=l2.val;
					if(l3 == null)
						ll=ll.next;
					else
						l3.next = l2.next;
					elementCount--;
					return rvl;
				}
			}
			
			l3=l2;
			
			l2 = l2.next;
		}
		
		return null;
	}
	
	public synchronized boolean removeElement(Object k)
	{
		Linker l2 = ll;
		Linker l3 = null;
		
		while(l2 != null)
		{
			if(l2.val == k)
			{
				if(l3 == null)
					ll=ll.next;
				else
					l3.next = l2.next;
				elementCount--;
				return true;
			}
			l3=l2;
			l2 = l2.next;
		}
		
		return false;
	}
	
	public Object thisElement()
	{
		return ll.val;
	}
	
	protected int elementCount;
	private Linker ll;
}
