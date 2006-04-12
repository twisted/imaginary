package twisted.util.parse;

import java.util.Vector;
import java.util.Enumeration;

public abstract class OrList extends ParseNode
{
	ParseNode success;
	
	protected abstract Vector init();
	
	protected void match(Token t) throws ParseException
	{
		Enumeration e = init().elements();
		while(e.hasMoreElements())
		{
			Object o = e.nextElement();
			success = (ParseNode) o;
			try
			{
				success.parse(t);
				return;
			}
			catch(ParseException pe)
			{
				//next...
			}
		}
		throw new ParseException();
	}
	
	public Token last()
	{
		return success.last();
	}
	public void printData(int x)
	{
		success.printData(x);
	}
	public Object data()
	{
		return success.data();
	}
}
