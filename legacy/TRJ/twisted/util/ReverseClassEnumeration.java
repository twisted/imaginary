package twisted.util;

import java.util.*;

public class ReverseClassEnumeration extends ClassBasedEnumeration
{
	public ReverseClassEnumeration(Enumeration e, Class c)
	{
		super(e,c);
	}
	public boolean filter(Object o)
	{
		return (o.getClass() != mc);
	}
}
