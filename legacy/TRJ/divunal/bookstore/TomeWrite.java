package divunal.bookstore;

import twisted.reality.*;

public class TomeWrite extends Verb
{
	class TomeWriteProc implements ResponseProcessor
	{
		Thing mt;
		int i;
		
		public TomeWriteProc(Thing t,int ii)
		{
			mt=t;
			i=ii;
		}
		
		public void gotResponse(String s)
		{
			mt.putString("page_#"+i,s);
		}
	}
	
	public TomeWrite()
	{
		super("write");
		setDefaultPrep("in");
	}
	public boolean action(Sentence d) throws RPException
	{
		Thing io = d.indirectObject("in");
		if(d.subject().isGod())
		{
			int i;
			
			try
			{
				i = Integer.parseInt(d.directString());
			}
			catch(NumberFormatException nfe)
			{
				// try 'next-prev-current'
				if(!d.hasDirect())
				{
					i=io.getInt("page_number");
				}
				else i=0;
			}
			if (i!= 0)
			{
				String xxx=io.getString("page_#"+i);
				if (xxx==null) xxx="A blank page.";
				d.subject().requestResponse(new TomeWriteProc(io,i),"Page " + i + " of " + io.nameTo(d.subject()),xxx);
			}
		}
		else
		{
			d.subject().hears("You don't seem like you have the authority, or the implements, to do that.");
		}
		return true; 
	}
}