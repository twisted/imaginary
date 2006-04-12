package demo;

import twisted.reality.*;

/**
 * This is the common "don't be involved with furniture anymore"
 * verb... It also intercepts any use of "go" as an attempt to leave
 * the furniture you are currently on/in.
 * 
 * This particular verb is for things with FrameSit, e.g. furniture
 * designed for giant robots.
 *
 * @author Tenth */

public class FrameStand extends Verb
{
	public FrameStand()
	{
		super("stand");
		alias("go");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		Player p = d.subject();
		Location g = p.place();
		Location f = (Location) d.verbObject();

		if(g.place() != f)
			return false;

		Object[] a = { "You stand from ",d.verbObject(),"." };
		g.place(f.place());
		d.subject().hears(a);

		return true;
	}
}
