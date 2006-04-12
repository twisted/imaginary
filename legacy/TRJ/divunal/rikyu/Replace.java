package divunal.rikyu;

import twisted.reality.*;

public class Replace extends Verb
{
    public Replace()
    {
	super("replace");
    }

    public boolean action(Sentence d) throws RPException
    {
	Location thePlace;
	try
	{
	    thePlace = (Location)d.directObject().getThing("replace");
	    if(thePlace == null)
		return false;
	}
	catch(ClassCastException e){ return false; }

	Object[] replaceMessage = {d.directObject(), " has been replaced."};
	d.directObject().moveTo(thePlace, replaceMessage);
	return true;
    }
}
