package demo;

import twisted.reality.*;

public class ToyDrop extends Verb
{
	public ToyDrop()
	{
		super("drop");
	}
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Location l = d.place();
		Thing theDoll = d.directObject();
		Thing isDoll = d.verbObject();

		if ((isDoll == theDoll) && (theDoll.place() == p))
		{
			Object[] squeak = {theDoll, " emits a faint squeak as it lands on the floor."};
			l.tellAll(squeak);
		}
		return false;
	}
}
