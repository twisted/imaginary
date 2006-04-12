package twisted.reality;

/**
 * This exception is thrown when somebody wants to do something with
 * something that can't do that. Like: <CODE> &lt;kill troll with
 * beanbag<br> You can't kill with a beanbag </code>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class NotWithThatException extends RPException
{
	public NotWithThatException(String s,String r){super(s);tn=r;}
	public String toString()
	{
		return "You can't " + getMessage() + " with a "+tn+".";
	}
	
	String tn;
}
