package divunal.tenth;

import twisted.reality.*;

public class LibraryDoorLook extends Verb
{
	public LibraryDoorLook()
	{
		super("look");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if(d.hasDirect())
		{
			if(d.directObject().place()==d.place())
			{
				throw new NoSuchThingException(d.directString());
			}
			else
				return false;
		}
		else if(d.hasIndirect("at"))
		{
			if(d.indirectObject("at").place()==d.place())
			{
				throw new NoSuchThingException(d.indirectString("at"));
			}
			else
				return false;
		}
		return true;
	}
}
