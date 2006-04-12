package divunal.bookstore;

import twisted.reality.*;

public class TomePage extends Verb
{
	public TomePage()
	{
		super("page");
		alias("turn");
		alias("read");
		setDefaultPrep("in");
	}
	public boolean action(Sentence d) throws RPException
	{
		Thing io;
		int i=0;
		if (d.hasDirectObject())
		{
			io=d.directObject();
			if (d.subject().getFocus() != io)
			{
				d.subject().setFocus(io);
			}
			else
			{
				i++;
				d.subject().hears("You turn to the next page.");
			}
		}
		else
		{
			io = d.indirectObject("in");

			if(d.hasDirect())
			{
				String dd = d.directString();
				
				if(dd.equals("forward") || dd.equals("next"))
				{
					i++;
					d.subject().hears("You turn to the next page.");
				}
				else if(dd.equals("backward") ||dd.equals("previous") ||dd.equals("prev"))
				{
					i--;
					d.subject().hears("You turn to the previous page.");
				}
				else
				{
					d.subject().hears("I don't know how to turn pages that way - use \"turn prev\" or \"turn next\"");
				}
			}
		}

		i+= io.getInt("page_number");		

		if(i>0)
		{
			String gs = io.getString("page_#"+i);
			
			if( gs !=null)
			{
				io.putInt("page_number",i);
				io.describe("The " +io.nameTo(d.subject())+ " is open to page " + i + ". It reads:\n\"" + gs + "\"");
			}
			else
			{
				d.subject().hears("There are no more pages that way.");
			}
		}
		else
		{
			return true;
		}
		
		return true;
	}
}
