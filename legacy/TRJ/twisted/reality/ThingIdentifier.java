package twisted.reality;

/**
 * This is a class which represents a reference to a Thing that the
 * server uses to keep track of Things without requiring their names
 * to stay constant.  This is really only useful if you're writing a
 * Persistable extension.
 * 
 * @see twisted.reality.Persistable
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public final class ThingIdentifier
{
	/* not publicly instantiatable */
	ThingIdentifier(){}
	
	/**
	 * The Thing that this ThingIdentifier represents.
	 */ 
	
	public Thing sThing()
	{
		return t;
	}
	
	/**
	 * The persistance of the Thing which this ThingIdentifier
	 * represents.
	 */
	
	public String toString()
	{
		if (t!=null) return t.persistance(); return "";
	}
	
	Thing t;
}
