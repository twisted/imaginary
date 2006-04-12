package twisted.reality;

/**
 * This is a stupid exception. It only happens if a verb asks for a
 * preposition without knowing if there's an indirect object. It has
 * an ugly format string. (In other words, there are very, very few
 * concievable ways in which this could happen.)
 * 
 * Ugh... I don't believe this is ever actually thrown in this version.
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class NoPrepositionException extends RPException
{
	public NoPrepositionException(){super();}
	public NoPrepositionException(String s) {super(s);}
}
