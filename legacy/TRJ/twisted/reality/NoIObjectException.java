package twisted.reality;

/**
 * This exception is thrown when a verb requests an indirect object
 * and the user did not specify one. Its format string reads, "What do
 * you want to [whatever] to?"
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class NoIObjectException extends RPException
{
	String prp;
	public NoIObjectException(String s,String prep){super(s);prp=prep;}
	public String toString()
	{
		return "What do you want to " + getMessage() + ' ' + prp + '?';
	}
}
