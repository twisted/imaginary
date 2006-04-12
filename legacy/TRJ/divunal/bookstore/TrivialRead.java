package divunal.bookstore;

import twisted.reality.*;

public class TrivialRead extends Verb
{
	public TrivialRead()
	{
		super("read");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		d.subject().hears(d.directObject().getString("book text"));
		return true;
	}
}
