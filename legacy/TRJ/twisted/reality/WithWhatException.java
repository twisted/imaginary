package twisted.reality;

/**
 * This exception is thrown when a player forgets to specify an
 * abletive object, and the verb requires it.  Its string format is
 * always, "And what do you propose to do that with?".
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class WithWhatException extends RPException
{
	public WithWhatException() { super(); }
	
	public String toString()
	{
		return "And what do you propose to do that with?";
	}
}
