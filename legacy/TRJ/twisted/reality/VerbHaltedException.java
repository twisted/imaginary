package twisted.reality;

/**
 * This exception is not intended to be caught - it only happens in
 * some very obscure circumstances where the wrong verb may begin to
 * execute.  Please allow your verbs to be halted by it.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class VerbHaltedException extends RPException
{
	public VerbHaltedException(){super();}
	public VerbHaltedException(String s){super(s);}
}
