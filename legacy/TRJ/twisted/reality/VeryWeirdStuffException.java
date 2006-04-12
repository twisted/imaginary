package twisted.reality;

/**
 * As you can tell from the classname, this is not an exception you
 * want to get. If you DO indeed get one, please send a stacktrace to
 * Glyph. (Umm... do we get these anymore?? I've never seen one
 * actually thrown...)
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class VeryWeirdStuffException extends RPException
{
	public VeryWeirdStuffException(){super();}
	public VeryWeirdStuffException(String s){super(s);}
}
