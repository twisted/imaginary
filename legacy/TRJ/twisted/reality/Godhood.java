package twisted.reality;

/**
 * This is the only class that is allowed to muck about with the "god"
 * bit at runtime.  Its syntax is "god username". (or, alternately,
 * for the overly religious, "g-d username")
 */

class Godhood extends Verb
{
	public Godhood()
	{
		super("god");
		alias("g-d");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = (Player) d.directObject();
		p.godBit=true;
		d.subject().hears("Done.");
		return true;
	}
}
