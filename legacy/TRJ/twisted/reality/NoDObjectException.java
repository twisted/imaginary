package twisted.reality;

/**
 * This exception is thrown when no direct object is present and one
 * is requested.
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class NoDObjectException extends RPException
{
	public NoDObjectException(String s){super(s);}
	public String toString()
	{
		return "What do you want to " + getMessage() + "?";
	}
}
