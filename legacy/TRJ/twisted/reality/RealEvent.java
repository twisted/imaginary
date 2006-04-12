package twisted.reality;

/**
 * This class represents an event - a happening being sent from one
 * object to another.
 *
 * @see RealEventHandler 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public final class RealEvent
{
	/**
	 * Create a new RealEvent with a type, argument, and target.
	 * @param type The type of event.
	 * @param arg The object argument.  Use this to encapsulate data, of
	 * whatever type you want.
	 * @param origin The object which is generating the event.
	 */
	
	public RealEvent(String type, Object arg, Thing origin)
	{
		ids=type;
		obj=arg;
		prp=origin;
	}
	
	String ids;
	Object obj;
	Thing prp;
	
	/**
	 * Returns the type of event.
	 */
	public String type()
	{
		return ids;
	}
	
	/**
	 * Returns the object argument.
	 */
	public Object arg()
	{
		return obj;
	}
	
	/**
	 * Returns the origin of the event.
	 */
	public Thing origin()
	{
		return prp;
	}
}
