package twisted.util.parse;

class IndirectsNode extends Truncator
{
	public ParseNode car(){return new IndirectNode();}
	public ParseNode cdr(){return new IndirectsNode();}
}
