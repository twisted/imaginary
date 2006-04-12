package twisted.util.parse;

import java.util.Vector;
import java.util.Enumeration;

public abstract class Sequence extends ParseNode
{
	protected abstract Vector init() throws ParseException;
	private ParseNode lastSuccess;
	protected Vector nodes;
	
	public Token last() { return lastSuccess.last(); }
	
	protected void match(Token t) throws ParseException
	{
		nodes = init();
		Enumeration e = nodes.elements();
		Token current = t;
		while (e.hasMoreElements())
		{
			Object o = e.nextElement();
			lastSuccess = (ParseNode) o;
			lastSuccess.parse(current);
			
			// make sure to keep up to the current position
			current=lastSuccess.last().next();
		}
	}
	/*
	  Create an array of each data() element from all elements in this
	  sequence
	 */
	// Luckily Object[] is a subclass of Object in java :-)
	public void printData(int tablen)
	{
		Object[] x = (Object[]) data();
		for(int i = 0; i<x.length; i++)
		{
			tab(tablen);
			System.out.println("data ["+i+"]: "+x[i]);
		}
	}
	public Object data()
	{
		Object[] ret = new Object[nodes.size()];
		Enumeration e = nodes.elements();
		int i=0;
		while(e.hasMoreElements())
		{
			ParseNode p = (ParseNode) e.nextElement();
			ret[i++]=p.data();
		}
		return ret;
	}
}
