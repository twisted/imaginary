package twisted.reality;

/**
 * A persistable form of the Stack data structure from twisted.util.
 * This is a demonstration of what you can do with the Persistable
 * class that's included with Twisted Reality.	See the source code
 * for details.
 * 
 * @version 1.0.1, 13 Aug 1999
 * @author Glyph Lefkowitz
 */

public class Stack implements Persistable
{
	twisted.util.Stack p;
	/**
	 * Constructs a new twisted.reality.Stack.  This kind of Stack can
	 * be persisted to files.
	 */
	public Stack()
	{
		p=new twisted.util.Stack();
	}
	
	/**
	 * Returns the elements of this stack.
	 */
	
	public java.util.Enumeration elements()
	{
		return p.elements();
	}
	
	/**
	 * Returns the map-persistent text that represents this Stack.
	 */
	
	public String persistance()
	{
		java.util.Enumeration e = new twisted.util.BackwardEnumeration (p.elements());
		StringBuffer rval = new StringBuffer();
		while(e.hasMoreElements())
		{
			Object q = e.nextElement();
			if (q instanceof String)
			{
				rval.append("string ").append(q);
			}
			else if (q instanceof Integer)
			{
				rval.append("int ").append(q);
			}
			else if (q instanceof Long)
			{
				rval.append("long ").append(q);
			}
			else if (q instanceof Double)
			{
				rval.append("double ").append(q);
			}
			else if (q instanceof Float)
			{
				rval.append("float ").append(q);
			}
			else if(q instanceof ThingIdentifier)
			{
				if (((ThingIdentifier) q).sThing() != null)
					rval.append("thing ").append(((ThingIdentifier)q).sThing().NAME());
			}
			rval.append("\n");
		}
		return rval.toString();
	}
	
	/**
	 * Pushes a String onto this Stack.
	 */
	
	public void pushString(String s)
	{
		p.push(s);
	}
	
	/**
	 * Pushes a Thing onto this Stack.
	 */
	
	public void pushThing(Thing t)
	{
		p.push(t.ref);
	}
	
	/**
	 * Looks at the top of this stack, if the top of the stack is a
	 * Thing.  Otherwise, returns null.
	 */
	
	public Thing peekThing()
	{
		Object o = p.peek();
		if (o instanceof ThingIdentifier)
			return ((ThingIdentifier) o).sThing();
		return null;
	}
	
	/**
	 * Pops the top off of the stack and returns it, if the top of the
	 * stack is a Thing.  Otherwise, returns null and does nothing.
	 */
	
	public Thing popThing()
	{
		Object o = p.peek();
		if (o instanceof ThingIdentifier)
		{
			p.pop();
			Thing th = ((ThingIdentifier)o).sThing();
			if (th!=null)
			{
				return th;
			}
			return popThing();
		}
		return null;
	}
	
	/**
	 * Peeks at the top of the stack, if it's a String.  Otherwise,
	 * returns null.
	 */
	
	public String peekString()
	{
		if (p.peek() instanceof String)
		{
			return ((String) p.peek());
		}
		return null;
	}
	
	/**
	 * Pops the top off of the stack and returns it, if the top of the
	 * stack is a String.  Otherwise, returns null and does nothing.
	 */
	
	public String popString()
	{
		if(p.peek() instanceof String)
		{
			return ((String) p.pop());
		}
		return null;
	}
	/**
	 * Pushes an integer onto the top of the stack.
	 */
	public void pushInt(int i)
	{
		p.push(new Integer(i));
	}
	/**
	 * Pops the top off of the stack and returns it, if the top of the
	 * stack is an Integer.  Otherwise, returns Integer.MAX_VALUE and
	 * does nothing.
	 */
	public int popInt()
	{
		if(p.peek() instanceof Integer)
		{
			return ((Integer)p.pop()).intValue();
		}
		return Integer.MAX_VALUE;
	}
	
		public boolean hasPop() 
		{
		return p.hasPop();
	}
	
	/**
	 * Initializes this Stack from a map-persistent String
	 * representing a stack.  This method is called by the Reality
	 * Pump -- there is no need to call it yourself.
	 */
	
	public void fromString(String s)
	{
		java.util.StringTokenizer q = new java.util.StringTokenizer(s,"\n",false);
		/*Age.log("StackFull: "+s);*/
		while (q.hasMoreElements())
		{
			String line = q.nextToken();
			/*Age.log("Stack: "+line);*/
			if (line.startsWith("string "))
			{
				p.push(twisted.util.StringLegalizer.delegalize(line.substring(7)));
			}
			else if (line.startsWith("thing "))
			{
				p.push(Age.theUniverse().findIdentifier(line.substring(6)));
			}
			else if (line.startsWith("float "))
			{
				p.push(Float.valueOf(line.substring(6)));
			}
			else if (line.startsWith("int "))
			{
				p.push(Integer.valueOf(line.substring(4)));
			}
			else if (line.startsWith("long "))
			{
				p.push(Long.valueOf(line.substring(5)));
			}
			else if (line.startsWith("double "))
			{
				p.push(Double.valueOf(line.valueOf(7)));
			}
		}
	}
	
	/**
	 * Returns the number of elements currently in the stack.
	 */
	
	public int size()
	{
		return p.size();
	}
}
