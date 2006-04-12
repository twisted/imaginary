package divunal.rikyu;

import twisted.reality.*;

public class Morph extends Verb
{
    public Morph()
    {
	super("morph");
	alias("transform");
	alias("unmorph");
	alias("untransform");
	setDefaultPrep("with");
    }

    public boolean action(Sentence d) throws RPException
    {
	if(d.verbString().startsWith("un"))
	{
	    String oldName = d.subject().name();
	    String oldGender = d.subject().getString("oldgender");
	    if(oldGender != null)
		d.subject().setGender(oldGender.charAt(0));
	    d.subject().removeProp("name");
	    d.subject().removeProp("description");
	    d.subject().removeProp("oldgender");
	    
	    Object[] toOther = {oldName, " morphs to reveal ", Name.of("true form",d.subject()),  ", ", d.subject(), "."};
	    Object[] toSubject = {"You return to your original form."};
	    d.subject().place().tellAll(d.subject(), toSubject, toOther);
	    d.subject().focusRefreshMyObservers();
	    return true;
	}
	else
 	{
	    String toMorph = d.directString();
	    String oldName = d.subject().name();
	    String toMorphName = d.verbObject().getString("morph name " + toMorph);
	    if(toMorphName == null)
		return false;

	    String toMorphDescr = d.verbObject().getString("morph descr " + toMorph);
	    String toMorphGender = d.verbObject().getString("morph gender " + toMorph);

	    d.subject().putString("name", toMorphName);
	    d.subject().putString("description", toMorphDescr);
	    if(toMorphGender != null)
	    {
		if(d.subject().getString("oldgender") == null)
			d.subject().putString("oldgender", "" + d.subject().getGenderTo(d.subject()));
		d.subject().setGender(toMorphGender.charAt(0));
	    }
	    Object[] toOther = {oldName, " morphs into ", d.subject(), "."};
	    Object[] toSubject = {"You morph into ",  d.subject().name(), "."};
	    d.subject().place().tellAll(d.subject(), toSubject, toOther);
	    d.subject().focusRefreshMyObservers();
	    return true;
	}
     }
}
