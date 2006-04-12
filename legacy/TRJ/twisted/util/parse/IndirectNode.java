package twisted.util.parse;

import java.util.Vector;

class IndirectNode extends Sequence
{
	public Vector init()
	{
		Vector v = new Vector();
		v.addElement (new TokenNode(StringToken.ST_PREP));
		v.addElement (new StringNode());
		return v;
	}
}
