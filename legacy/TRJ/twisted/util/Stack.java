package twisted.util;

/*
 * I love writing stacks.  They're the world's simplest data structure.
 */

public class Stack
{
	class Stk
	{
		Stk(Object data, Stk next)
		{
			this.data=data;
			this.next=next;
		}
		Stk next;
		Object data;
	}
	
	class StkEnum implements java.util.Enumeration
	{
		StkEnum(Stk s)
		{
			stk=s;
		}
		public boolean hasMoreElements()
		{
			return (stk!=null);
		}
		public Object nextElement()
		{
			if (stk!=null)
			{
				Object o=stk.data;
				stk=stk.next;
				return o;
			}
			return null;
		}
		
		Stk stk;
	}
	
	Stk stk;
	
	public Stack()
	{
		
	}
	
	public java.util.Enumeration elements()
	{
		return new StkEnum(stk);
	}
	
	public void push(Object o)
	{
		stk=new Stk(o,stk);
		elementCount++;
	}
	
	public boolean hasPop()
	{
		return (stk!=null);
	}
	
	public Object pop()
	{
		if (stk==null) return null;
		Object o = stk.data;
		stk=stk.next;
		elementCount--;
		return o;
	}
	
	public Object peek()
	{
		if (stk == null) return null;
		return stk.data;
	}
	
	public void popAll()
	{
		stk=null;
		elementCount=0;
	}
	
	public int size()
	{
		return elementCount;
	}
	int elementCount;
}
