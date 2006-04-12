package divunal.bookstore;

import twisted.reality.*;

public class Lookup extends Verb
{
	public Lookup()
	{
		super("lookup");
		alias("look");
		alias("index");
		setDefaultPrep("in");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing book;
		String word=null;
		if (d.verbString().equals("look"))
		{
			if(d.hasDirect() && d.directString().startsWith("up "))
			{
				word=d.directString().substring(3);
			}
			else
			{
				return false;
			}
		}
		
		book=d.verbObject();
		if(d.hasDirect() && (d.hasDirectObject()?(book != d.directObject()):true))
		{
			if(word==null)
				word = d.directString();
			
			String defn = book.getString("enc define "+word.toLowerCase());
			if (defn!=null)
			{
				Object[] toHear =
				{
					"You look up ",word," in ",book,
					" and find an entry.  It reads:\n",defn
				};
				d.subject().hears(toHear);
			}
			else
			{
				d.subject().hears("You don't find anything interesting.");
			}
		}
		else
		{
			Stack s = (Stack) book.getPersistable("enc index");
			

			java.util.Enumeration e;
			if (s==null || !(e=s.elements()).hasMoreElements())
			{
				Object[] empty = {Name.Of(book)," is empty."};
				d.subject().hears(empty);
				return true;
			}
			if(e.hasMoreElements())
			{
				Object[] sporty = {Name.Of(book)," sports an index, listing the following topics:"};
				d.subject().hears(sporty);
				
				while (e.hasMoreElements())
				{
					d.subject().hears((String)e.nextElement());
				}
			}
		}
		return true;
	}
}
