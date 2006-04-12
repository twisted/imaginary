package twisted.reality;

/**
 * This exception is thrown if a user wants to do something that the
 * game simply doesn't know how to handle in the current context.  It
 * reports a variety of quirky error messages.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class NoSuchVerbException extends RPException
{
	public NoSuchVerbException(String s){super(s);}
	
	public static final String[] errors =
	{
		"You don't think that you want to waste your time with that.",
		"There are probably better things to do with your life.",
		"You are nothing if not creative, but that creativity could be better applied to developing a more productive solution.",
		"Perhaps that's not such a good idea after all.",
		"Surely, in this world of limitless possibility, you could think of something better to do.",
		"An interesting idea...",
		"A valiant attempt.",
		"What a concept!",
		"You can't be serious."
	};
	
	public String toString()
	{
		return Verb.random(errors);
	}
}
