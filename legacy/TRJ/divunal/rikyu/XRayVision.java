package divunal.rikyu;

import twisted.reality.*;
import twisted.reality.plugin.*;
import java.util.Enumeration;
import java.util.Vector;

public class XRayVision extends Verb
{
	public XRayVision()
	{
		super("look");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Look l = new Look();
		l.action(d);
		
		if(d.verbObject().getBool("clothing worn") && (! d.hasDirect()))
		{
			Vector result = new Vector(10);
			Enumeration things = d.subject().topPlace().things();
			if(things.hasMoreElements())
				result.addElement("Your X-Ray Spectacles (tm) reveal that the room also contains ");
			
			while(things.hasMoreElements())
			{
				Thing t = (Thing)things.nextElement();
				if( (! t.isComponent()) || t.equals(d.subject()))
					continue;

				if(! things.hasMoreElements() && result.size() > 1)
					result.addElement("and ");

				result.addElement(t);

				if(things.hasMoreElements())
					result.addElement(", ");
				else
					result.addElement(".");
			}
			
			if(result.size() > 1)
				d.subject().hears(result);
		}
		return true;
	}
}
