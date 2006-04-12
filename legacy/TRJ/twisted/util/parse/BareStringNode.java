package twisted.util.parse;

import java.util.Vector;

class BareStringNode extends Truncator
{
	public ParseNode car() 
	{ 
		return 
			new OrList()
			{
				public Vector init()
				{
					Vector v = new Vector();
					v.addElement(new TokenNode(StringToken.ST_WORD));
					v.addElement(new TokenNode(StringToken.ST_PREP));
					return v;
				}
			};
	}
	public ParseNode cdr()
	{
		return new BareStringNode();
	}
	
	public Object data()
	{
		if(b!=null)
		{
			return (((String) a.data()) + " " + ((String) b.data()));
		}
		else
		{
			return a.data();
		}
	}
}
