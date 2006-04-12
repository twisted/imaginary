package twisted.util.parse;

class ParseDemo extends ParseNode
{
	public ParseDemo()
	{
		// My grammar (tee hee)

		// tokens: word quote preposition abletive term end
		//
		// Verb => word
		//
		// DirectPart => string
		//
		// IndirectPart => preposition string
		//
		// IndirectParts => IndirectPart
		//                | IndirectPart IndirectParts
		// 
		// string => word string
		//         | word
		//         | quotedString
		//         | quotedString string
		// 
		// quotedString => quote bareString quote
		//
		// bareString => anyWord bareString
		//             | anyWord
		//
		// anyWord => word
		//          | preposition
		//
		// Sentence => Verb DirectPart IndirectParts 
		//           | Verb DirectPart 
		//           | Verb IndirectParts
		//           | Verb
		// 
		// Paragraph => Sentence
		//            | Sentence term Paragraph
		//            | END
		
	}
	public void parseString(String s) throws ParseException
	{
		StringToken sqt = new StringToken(s);
		parse(sqt.next());
		printData(0);
	}

	public void printData(int x)
	{
		pn.printData(x);
	}

	public Token last()
	{
		return null;
	}
	
	public void match(Token t) throws ParseException
	{
		if(t.type()==StringToken.ST_END)
		{
			System.out.println("Game Over");
			System.exit(0);
		}
		pn.parse(t);
	}
	
	SentenceNode pn = new SentenceNode();
	
	Sentence mySentence;
	
	public Object data()
	{
		return mySentence;
	}
	public static void main(String[] args)
	{
		ParseDemo pd = new ParseDemo();
		try{pd.parseString("talk to \"to me to me\"");}
		catch(Exception e){ System.out.println("Oh shit.");}
	}
}
