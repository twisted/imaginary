package twisted.reality;

/**
 * This exception gets thrown when a word which is not recognizeably
 * parseable shows up in the wrong place in a file.  If you see this
 * displayed in the server's output, stop the server and check your
 * mapfile.  Something is wrong with it.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class BadWordException extends RPParseException
{
	public BadWordException() {super();}
	public BadWordException(String s) {super(s);}
}
