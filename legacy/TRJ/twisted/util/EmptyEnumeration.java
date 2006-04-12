package twisted.util;
import java.util.*;

/**
 * Just what it sounds like.
 */

public class EmptyEnumeration implements java.util.Enumeration
{
	/** You only ever need one of these things, so here it is. **/
	
	public static final EmptyEnumeration EMPTY=new EmptyEnumeration ();
	
	/**
	 * Allocating one of these would be a waste of memory, so it's
	 * private.
	 **/
	private EmptyEnumeration()
	{
		
	}
	
	/**
	 * Returns false.
	 */
	
	public boolean hasMoreElements()
	{
		return false;
	}
	
	/**
	 * Returns null.
	 */
	
	public Object nextElement()
	{
		return null;
	}
}
