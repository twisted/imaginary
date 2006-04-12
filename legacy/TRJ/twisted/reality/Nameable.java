package twisted.reality;

/**
 * This represents an object which can be named.  Portals, Things,
 * Players, Rooms -- all of these things are nameable.
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Nameable
{
	/**
	 * This changes the name of the nameable object to a new one.
	 */
	
	public void name(String x)
	{
		myName = x!=null ? Age.intern(x) : null;
	}
	
	/**
	 * The name of this Nameable as it will normally appear.  Note
	 * that this is not always the accurate and true name of the
	 * object.  If you are displaying the name of an object it is
	 * almost always preferable to use this method.
	 */
	
	public String name()
	{
		return myName;
	}
	
	/**
	 * This method always returns the accurate, unaltered name of the
	 * object as it was last stored by the name() function.  This
	 * will, for example, always return the unique identifier with
	 * which a Thing may be searched for within an Age.  If you are
	 * displaying the name of an object it is almost always preferable
	 * to use name() instead.
	 * 
	 * @see twisted.reality.Age.findThing(java.lang.String)
	 */
	
	public final String NAME()
	{
		return myName;
	}
	/**
	 * Create a new Nameable with the specified name.
	 * 
	 * @param nm The initial name of this object.
	 */
	protected Nameable(String nm)
	{
		if (nm!=null)
			name(nm);
	}
	
	String myName;
}
