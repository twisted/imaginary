package twisted.reality;

/**
 * This exception gets thrown if the object you're looking for isn't
 * here. (This is conceptually identical to NoSuchObjectException now.)
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class NotHereException extends RPException
{
	public NotHereException(String s)
	{
		super(s);
	}
	
	public String toString()
	{
		return "There's no " + getMessage() + " here.";
	}
}
