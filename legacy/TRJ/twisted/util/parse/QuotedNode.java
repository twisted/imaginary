package twisted.util.parse;

import java.util.Vector;

class QuotedNode extends Sequence
{
	public Vector init()
	{
		Vector v = new Vector();
		
		v.addElement(new TokenNode(StringToken.ST_QUOTE));
		v.addElement(new BareStringNode());
		v.addElement(new TokenNode(StringToken.ST_QUOTE));
		return v;
	}
	
	
	
	public Object data()
	{
		// return the middle string.  The first and last are just quotes.
		return ((Object[])super.data())[1];
	}
}
