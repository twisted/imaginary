package twisted.reality;

/**
 * A persistable form of the Vector data structure from java.util.
 * This is a demonstration of what you can do with the Persistable
 * interface that's included with Twisted Reality. See the source code
 * for details.
 * 
 * Please note that this class uses the default Vector methods for
 * storing and retrieving data, but it can only persist the types:
 * String Integer Long Double Float ThingIdentifier.  If you like to
 * have your code automatically checked by the runtime for things like
 * incorrect types, please use the provded "put" method.  Because
 * addElement is final, it cannot be overridden.
 * 
 * Please note that this class has not been heavily tested.  (Read: we
 * have never used this so we don't know what it does.)
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class VectorList extends java.util.Vector implements Persistable
{
	public String persistance()
	{
		java.util.Enumeration e = elements();//new twisted.util.BackwardEnumeration (p.elements());
		StringBuffer rval = new StringBuffer();
		while(e.hasMoreElements())
		{
			Object q = e.nextElement();
			if (q instanceof String)
			{
				rval.append("string ").append(q);
			}
			else if (q instanceof Integer)
			{
				rval.append("int ").append(q);
			}
			else if (q instanceof Long)
			{
				rval.append("long ").append(q);
			}
			else if (q instanceof Double)
			{
				rval.append("double ").append(q);
			}
			else if (q instanceof Float)
			{
				rval.append("float ").append(q);
			}
			else if(q instanceof ThingIdentifier)
			{
				if (((ThingIdentifier) q).sThing() != null)
					rval.append("thing ").append(((ThingIdentifier)q).sThing().NAME());
			}
			rval.append("\n");
		}
		return rval.toString();
	}
	
	/**
	 * This method is preferred to addElement because it will
	 * automatically convert Things to ThingReferences, and it will
	 * perform type-checking so you won't accidentally attempt to put
	 * a type into a VectorList that can't be persisted.
	 */
	
	public void put(Object o)
	{
		if ( o instanceof String ||
			 o instanceof Number )
		{
			super.addElement(o);
		}
		else if ( o instanceof Thing )
		{
			super.addElement(((Thing)o).ref);
		}
		throw new IllegalArgumentException("The only things you can add to a Vector are Things, Strings, and Numbers");
	}
	
	public void fromString(String s)
	{
		java.util.StringTokenizer q = new java.util.StringTokenizer(s,"\n",false);
		/*Age.log("StackFull: "+s);*/
		while (q.hasMoreElements())
		{
			String line = q.nextToken();
			/*Age.log("Stack: "+line);*/
			if (line.startsWith("string "))
			{
				addElement(twisted.util.StringLegalizer.delegalize(line.substring(7)));
			}
			else if (line.startsWith("thing "))
			{
				addElement(Age.theUniverse().findIdentifier(line.substring(6)));
			}
			else if (line.startsWith("float "))
			{
				addElement(Float.valueOf(line.substring(6)));
			}
			else if (line.startsWith("int "))
			{
				addElement(Integer.valueOf(line.substring(4)));
			}
			else if (line.startsWith("long "))
			{
				addElement(Long.valueOf(line.substring(5)));
			}
			else if (line.startsWith("double "))
			{
				addElement(Double.valueOf(line.valueOf(7)));
			}
		}
	}
}
