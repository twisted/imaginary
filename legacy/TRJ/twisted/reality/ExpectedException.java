package twisted.reality;

/**
 * This exception is thrown when a certain word is expected in a POR
 * file and it's not found.  If you notice one, check your map-file --
 * something's wrong with it.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class ExpectedException extends RPParseException
{
	public ExpectedException() {super();}
	public ExpectedException(String s) {super(s);}
}
