package divunal.tenth;

import twisted.reality.*;
import divunal.Divunal;

public class TiringVerb extends Verb
{
    public TiringVerb()
    {
		super("tire");
		setDefaultPrep("with");
    }
	
    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		String towhat;
		Player tiree;
		float tammount;
		Room r = (Room) d.place();

		if (!(p.isGod()))
		{
			p.hears("You're not quite sure how this thing works, exactly...");
			return true;
		}

		tiree = (Player) d.directObject();
	
		tammount = 0.3f;

		if (d.hasIndirect("by"))
		{
			towhat = d.indirectString("by");
			try
			{
				tammount = Float.valueOf(towhat).floatValue();
			}
			catch(NumberFormatException nfe)
			{
				d.subject().hears("A strangely soothing but disembodied female voice says, \"Please express the ammount as a floating point number.\"");
			}
		}

		if (tiree == p)
		{
			Object[] x = {"You give yourself a good jolt, and your life seems to drain out of you..."};
			Object[] stunz = {p," shoots ",Name.of(p,p)," with a scintillating beam of light, and looks momentarily stunned."};
			r.tellAll(p,x,stunz);
		}
		else 
		{
			Object[] tiredhears={p," points at you, and you are struck by a beam of light..."};
			Object[] elsehears={p," strikes ",tiree," with a beam of scintillating light, stunning ",Pronoun.of(tiree)," momentarily."};
			Object[] subjhears={"You zap ",tiree,"."};
			r.tellAll(p,tiree,subjhears,tiredhears,elsehears);
		} 
		Divunal.majorStun(tiree, tammount);

		return true;
	}
}