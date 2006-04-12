package twisted.reality;

import twisted.util.LinkedList;

/**
 * This deals with ambiguity and vagueness.
 */

class AmbiguityRecord extends twisted.util.LinkedList
{
	public AmbiguityRecord(Thing a, Thing b) 
	{
		super();
		addElement(a);
		addElement(b);
	}
	
	public Thing lessAmbiguous(Thing c)
	{
		if(removeElement(c))
		{
			if(elementCount == 1)
				return (Thing) thisElement();
		}
		return null;
	}
	
	public void moreAmbiguous(Thing d)
	{
		addElement(d);
	}
}
