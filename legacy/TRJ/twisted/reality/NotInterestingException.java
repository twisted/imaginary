package twisted.reality;
import java.util.Random;

/**
 * This exception gets thrown when the object that a user specifies is
 * mentioned in the description of the place they're in, but isn't
 * terribly useful or sensible to interact with.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class NotInterestingException extends RPException
{
	String verbName;
	
	public NotInterestingException(String s, String n)
	{
		super(s);
		verbName = n;
	}

	public String toString()
	{
		return "You see nothing particularly interesting about the " + getMessage() + ".  You certainly don't think it would be interesting to " + verbName + " it.";
	}
}
