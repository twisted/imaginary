package twisted.reality;

/**
 * This class represents a dynamic property.  It is meant to be
 * overridden to give it functionality.  It can be used on a Thing in
 * place of a normal static property so that different players can see
 * the same object differently. The value function must be implemented
 * by your subclass to reutrn a supported property type.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public abstract class DynamicProperty
{
	/**
	 * Create a new DynamicProperty.
	 */
	
	public DynamicProperty()
	{
		// do nothing
	}
	/**
	 * This is the method you must override to make your property
	 * work.  The value returned here will be translated and returned
	 * by getXXX and setXXX from whatever Thing(s) this
	 * DynamicProperty is eventually stored on.
	 *
	 * @param origin The thing which has the property on it that's
	 * being retrieved.
	 *
	 * @param destination The thing which is trying to retrieve the
	 * property (IE, the Player who is requesting the room's
	 * description...)
	 *
	 * @returns a String, Thing, Integer, Boolean, Persistable, or
	 * other supported property type.
	 */
	public abstract Object value(Thing origin, Thing destination);

	/** 
	 * This is exactly the same as Verb.random(), included here for 
	 * convenience's sake. 
	 * 
	 * @see twisted.reality.Verb 
	 */ 
	 
	public static int random() 
	{ 
		return Verb.random(); 
	} 
	 
	/** 
	 * This is exactly the same as Verb.randomf(), included here for 
	 * convenience's sake. 
	 *	
	 * @see twisted.reality.Verb 
	 */ 
	 
	public static float randomf() 
	{ 
		return Verb.randomf(); 
	} 
	 
	/** 
	 * This is exactly the same as Verb.random(String[]), included 
	 * here for convenience's sake. 
	 * 
	 * @see twisted.reality.Verb 
	 */ 
	 
	public String random(String[] stuff) 
	{ 
		return Verb.random(stuff); 
	} 
}
