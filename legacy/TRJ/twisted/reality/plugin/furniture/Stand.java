package twisted.reality.plugin.furniture;

import twisted.reality.*;

/**
 * This is the common "don't be involved with furniture anymore"
 * verb... It also intercepts any use of "go" as an attempt to leave
 * the furniture you are currently on/in.
 * 
 * @author Tenth */

public class Stand extends Verb
{
	public Stand()
	{
		super("stand");
		alias("go");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		if(d.subject().place() != d.verbObject())
			return false;
		Object[] a = { "You stand from ",d.verbObject(),"." };
		d.subject().place(d.verbObject().place());
		d.subject().hears(a);

		return true;
	}
}
