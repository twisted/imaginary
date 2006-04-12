package twisted.util.parse;

public abstract class ParseNode
{
	public void tab(int depth)
	{
		for(int i=0; i<depth; i++)
		{
			System.out.print('\t');
		}
	}
	

	// this is final because it should never be changed.  Override "match"
	public final void parse(Token t) throws ParseException
	{
		fst=t;
		match(t);
	}
	protected abstract void match(Token t) throws ParseException;
	
	public Token first()
	{
		return fst;
	}
	
	// give back the last token which *is* a part of this pattern.
	// Zero-token patterns are implicitly disallowed by this... but
	// then again, they're sort of implicitly disallowed by common
	// sense
	
	public abstract Token last();
	
	// data for first()
	private Token fst;
	
	// this next one's kind optional, but it allows you to do some
	// second-pass parsing stuff so you don't have to worry about
	// extracting any data at first.  I personally think it's useful
	// generically, but for this specific case it might not be.
	// Dunno.
	public abstract Object data();

	// for debugging only
	
	public void printData(int tabDepth)
	{
		tab(tabDepth);
		System.out.println("No Printage: " + getClass().getName() + " data: " + data());
	}
}
