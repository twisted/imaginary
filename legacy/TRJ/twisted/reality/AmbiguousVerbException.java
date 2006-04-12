package twisted.reality;

/**
 * TODO: phase this out.  It's rather obsolete and it's unclear to the
 * player what's happening when it gets thrown (forget about explaining
 * this to the developer...)
 */

class AmbiguousVerbException extends RPException
{
	AmbiguousVerbException(String t)
	{
		super(t);
	}
	
	public String toString()
	{
		return "I am not sure which object to associate the action \"" + getMessage() + "\" with.  Specify fewer objects, if possible.";
	}
}
