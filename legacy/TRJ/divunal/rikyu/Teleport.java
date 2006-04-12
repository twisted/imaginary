package divunal.rikyu;

import twisted.reality.*;
//this is a kool verb
public class Teleport extends Verb
{
    public Teleport()
    {
		super("teleport");
    }
    
    public boolean action(Sentence d) throws RPException
    {
		Location loc = null;
		Thing t = null;
	
		if(d.hasIndirect("to"))
		{
			try
			{
				loc = (Location)Age.theUniverse().findThing(d.indirectString("to"));
			}
			catch(ClassCastException e)
			{
				d.subject().hears("You can only teleport things into locations.");
				return true;
			}
			t = d.directObject();
		}
		else
		{
			try
			{
				loc = (Location)Age.theUniverse().findThing(d.directString());
			}
			catch(ClassCastException e)
			{
				d.subject().hears("I think you'd be really displeased if you teleported there.");
				return true;
			}
			t = d.subject();
		}
	
		if(loc == null)
			return false;
	
		Object[] leaveHeard = {t, " " + (t.getString("teleport out") == null ? "disappears in a puff of smoke." : t.getString("teleport out"))};
		Object[] arriveHeard = {t, " " + (t.getString("teleport in") == null ? "appears in a puff of smoke." : t.getString("teleport out"))};
		
		Object[] leaveSubjectHeard = {"You feel reality bend around you for a moment..."};
		Object[] arriveSubjectHeard = {"You've been teleported to ", loc};

		Object[] leaveArgs = {t, " vanishes."};
		Object[] arriveArgs = {t, " appears."};
		
		t.place().tellAll(t, leaveSubjectHeard, leaveHeard);
		t.moveTo(loc, leaveArgs, arriveArgs);
		t.place().tellAll(t, arriveSubjectHeard, arriveHeard);
		
		return true;
    }
}