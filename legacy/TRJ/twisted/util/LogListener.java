package twisted.util;

/**
 * This is the interface you must implement to listen to the system log.
 *
 * @see twisted.reality.Age.log
 * @version 1.0.0pre2, 12 Jun 1999
 * @author James Knight
 */

public interface LogListener
{
	/**
	 * Log this message.
	 */
	void log(int debug, java.util.Date date, String message);
}
