package twisted.util.parse;

import java.util.Vector;

class SentenceNode extends Truncator
{
	/*
	 * this is the Verb
	 */
	public ParseNode car() { return new TokenNode(StringToken.ST_WORD);}

	/*
	 * This is the rest of the sentence after the verb.
	 */
	public ParseNode cdr() 
	{ 
		return new OrList()
		{
			public Vector init()
			{
				Vector xx = new Vector();
				xx.addElement
					(new Truncator()
					{
						// this is the direct object
						public ParseNode car()
						{
							// right here
							return new StringNode();
						}
						public ParseNode cdr()
						{
							// one possible place for the indirect object
							return new IndirectsNode();
						}
					});
				xx.addElement(new IndirectsNode());
				return xx;
			}
		};
	}
}
