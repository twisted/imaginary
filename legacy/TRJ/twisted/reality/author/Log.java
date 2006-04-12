package twisted.reality.author;

import twisted.reality.*;

/**
 * Logs a message to the logfile.
 */

public class Log extends Verb
{
	public Log()
	{
		super ("log");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		String str = d.directString();
		Age.theUniverse().log(str);
		d.subject().hears("Log Message: " + str);
		return true;
	}
}
