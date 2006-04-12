package twisted.util.parse;

public abstract class Truncator extends ParseNode
{
	// please pardon the lisp humor, and feel free to rename these to
	// something that actualy makes sense.  this is a slight
	// optimization for grammar elements like
	// 
	// DeclList => DeclList
	//             | DeclList, Decl
	//
	// Rather than making sure these are put in the right order in a
	// sequence, or parsing the same DeclList twice:
	
	protected abstract ParseNode car();
	protected abstract ParseNode cdr();
	
	protected ParseNode a;
	protected ParseNode b;
	protected void match(Token t) throws ParseException
	{
		a=car();
		b=cdr();
		
		// You need A, but
		a.parse(t);
		
		try
		{
			// B is optional.
			b.parse(a.last().next());
		}
		catch(ParseException pe)
		{
			// If the match fails, just make it go away.
			b=null;
		}
	}
	public Object data()
	{
		if(b!=null)
		{
			Object p = a.data();
			Object q = b.data();
			
			Object[] r = new Object[2];
			r[0]=p;
			r[1]=q;
			return r;
		}
		else
		{
			// in the above example, you're the "just Decl" version of
			// "DeclList".  All the data you have is the Decl's
			// data... so just return it.
			// For your reference, casting to arrays works like this:
			// 
			// Truncator t = new Trunctor();
			// ... do stuff ...
			// Object[] stuff = (Object[]) t.data(); 
			return a.data();
		}
	}
	
	public void printData(int tabDepth)
	{
		if(b!=null)
		{
			tab(tabDepth);
			System.out.println("Truncator");
			tab(tabDepth);
			System.out.println("[");
			tab(tabDepth+1);
			System.out.println("A:");
			a.printData(tabDepth+1);
			System.out.println();
			tab(tabDepth+1);
			System.out.println("B:");
			b.printData(tabDepth+1);
			tab(tabDepth);
			System.out.println("]");
		}
		else
		{
			a.printData(tabDepth);
		}
	}
	
	public Token last()
	{
		if(b!=null) return b.last(); else return a.last();
	}
}
