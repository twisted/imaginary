package divunal.dream;

import twisted.reality.*;

public class TakeShroom extends Verb
{
	public TakeShroom()
	{
		super("take");
		alias("get");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		d.subject().hears("It's a bad idea to take shrooms.");
		return true;
	}
}
