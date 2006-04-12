package twisted.reality;

/**
 * This is the superclass of all Reality Pump exceptions.
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class RPException extends Exception
{
	public RPException(){super();}
	public RPException(String s){super(s);}
	public String toString()
	{
		return getMessage();
	}
}
