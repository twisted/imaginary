package divunal.rikyu;

import twisted.reality.*;

public class LinkingBookOpen extends Verb
{
	public LinkingBookOpen()
	{
		super("open");
		alias("read");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing linkingBook = d.directObject();
		Location l = (Location)linkingBook.getThing("linkTo");
		Location startPoint = d.place();
		if(l != null)
		{
			d.subject().hears("You feel a strange sensation in your limbs...");
			
			Object[] leaving = 
			{
				"All of a sudden, you are blinded by a bright light! When your vision returns, ",
				d.subject(), " is gone. The book ",
				Pronoun.of(d.subject()), " was holding falls to the floor."
			};
			Object[] dropbook =
			{
				"The book ",
				d.subject(),
				" was holding falls to the floor."
			};
			Object[] entering = 
			{
				"All of a sudden, you are blinded by a bright light! When your vision returns, you see that ",
				d.subject(), " has appeared."
			};
			
			d.subject().moveTo(l, leaving, entering);
			linkingBook.moveTo(startPoint,dropbook);
			d.subject().hears("You look up and realize you are no longer where you were. The book you were reading is now gone.");
			return true;
		}
		return false;
	}
}
