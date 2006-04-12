package twisted.util.parse;

import java.util.Vector;

class StringNode extends OrList
{
	public Vector init()
	{
		Vector v = new Vector();
		v.addElement
		(
		 new Truncator()
		 {
			 public ParseNode car() { return new QuotedNode(); }
			 public ParseNode cdr() { return new StringNode(); }
		 }
		 );
		v.addElement
		(
		 new Truncator()
		 {
			 public ParseNode car() { return new TokenNode(StringToken.ST_WORD); }
			 public ParseNode cdr() { return new StringNode(); }
		 }
		 );
		return v;
	}

	public Object data()
	{
		Object o = super.data();
		if(o instanceof Object[])
		{
			String[] s = (String[]) o;
			return (s[0]+" "+s[1]);
		}
		else
		{
			return o;
		}
	}
}
