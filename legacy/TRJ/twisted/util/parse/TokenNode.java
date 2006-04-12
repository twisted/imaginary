package twisted.util.parse;

class TokenNode extends ParseNode
{
	// What type of token should I be?
	public int myType;
	// this is private because the data() method should return
	// whatever relevant data you need...
	private Token myToken;
	
	public TokenNode(int a)
	{
		myType=a;
	}
	
	protected void match(Token t) 
		throws ParseException
	{
		if(t.type()==myType)
		{
			myToken=t;
		}
		else
		{
			throw new ParseException();
		}
	}
	public Token last()
	{
		return myToken;
	}
	
	public Object data()
	{
		return myToken.data();
	}
	
	
	public void printData(int tabDepth)
	{
		tab(tabDepth);
		System.out.println("Token: " + getClass().getName() + " Data: \"" + data() + "\" Type: " + myToken.type());
	}
}
