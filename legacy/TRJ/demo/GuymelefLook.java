package demo;

import twisted.reality.*;

// This is a generic Open/Close verb for
// containers.

public class GuymelefLook extends Verb
{
	public GuymelefLook()
	{
		super ("look");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing g = d.verbObject();
		Player p = d.subject();
		Location l = d.place();
		String verb = d.verbString();

		if (l == g)
		{
			p.setFocus(g.place());
			return true;
		}

		return false;
	}
}
