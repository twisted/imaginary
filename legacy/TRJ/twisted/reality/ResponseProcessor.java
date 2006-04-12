package twisted.reality;

import java.util.Date;
/**
 * This interface defines the class that you must implement to use the
 * requestResponse() method in Player.  requestResponse will pop up a
 * window, and when gotResponse is called in your ResponseProcessor,
 * the string that it is called with will be the text that the player
 * entered into that window when they hit OK.
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public interface ResponseProcessor
{
	/**
	 * The method that's called when the response is given.
	 * 
	 * @param s the response
	 */
	void gotResponse(String s);
}
