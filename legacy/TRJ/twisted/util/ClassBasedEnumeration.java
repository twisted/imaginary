package twisted.util;

import java.util.*;

/**
 * This class filters an enumeration by only returning those elements
 * that are of the specified Class.
 *
 * @version 0.99.99 12/12/1999
 * @author Glyph Lefkowitz
 */

public class ClassBasedEnumeration extends FilterEnumeration
{
	public ClassBasedEnumeration(Enumeration e,Class c)
	{
		super(e);
		mc = c;
	}
	
	public boolean filter(Object o)
	{
		return (o.getClass() == mc);
	}
	
	Class mc;
}
