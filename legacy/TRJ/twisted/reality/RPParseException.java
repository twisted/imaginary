package twisted.reality;

/**
 * This exception is thrown when there is an error parsing a
 * Persistence of Reality file.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class RPParseException extends RPException
{
	public RPParseException() {super();}
	public RPParseException(String s) {super(s);}
}
