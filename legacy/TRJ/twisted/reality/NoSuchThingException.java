package twisted.reality;

/**
 * This exception gets thrown when the object that a user specifies
 * doesn't exist.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class NoSuchThingException extends RPException
{
	public NoSuchThingException(String s){super(s);}
	public String toString()
	{
		return "There is no " + getMessage() + " here.";
	}
}
