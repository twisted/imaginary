package divunal.bookstore;

import twisted.reality.*;

// A slightly modified version of TrivialRead for things which
// theoretically could also be opened or closed (like books)

public class TrivialOpenRead extends Verb
{
	public TrivialOpenRead()
	{
		super("read");
		alias("open");
		alias("close");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Thing theBook = d.directObject();
		String readVerb = d.verbString();
		Room r = (Room)d.place();

		Object [] othersSee = {p, " reads ",theBook,"."};
		Object [] pOpens = {"You open ",theBook," and glance through it."};
		Object [] pReads = {"You read ",theBook,"."};

		if (readVerb.equals("read"))
		{
			r.tellAll(p, pReads, othersSee);
			p.hears(theBook.getString("book text"));
		}
		else if (readVerb.equals("open"))
		{
			if (p.getFocus() == theBook)
				r.tellAll(p, pReads, othersSee);
			else
			{
				r.tellAll(p, pOpens, othersSee);
				p.setFocus(theBook);
			}
			p.hears(theBook.getString("book text"));
		}
		else if (readVerb.equals("close"))
		{
			if (p.getFocus() == theBook)
			{
				Object[] pCloses = {"You close ",theBook,"."};
				Object[] oCloses = {p," closes ",theBook,"."};
				r.tellAll(p, pCloses, oCloses);
				p.setFocus(r);
			}
			else
				p.hears("You don't have it open right now, making it hard to close.");
		}

		return true;
	}
}
