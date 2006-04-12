/* Looping event initiator by Tenth & Glyph (5/5/99)
   Activate <thing> (activates "startup" event by default)
   Activate <event> on <thing> (activates <event> on <thing>)
*/

package divunal.common;
import twisted.reality.*;

public class Activate extends Verb
{
	public Activate()
	{
		super("activate");
		setDefaultPrep("with");
	}

	public boolean action(Sentence d) throws RPException
	{
		if (d.hasDirect())
		{
			if (d.hasIndirect("on"))
			{
				d.indirectObject("on").handleEvent(new RealEvent(d.directString(), null,null));
				d.subject().hears(d.directString()+" event activated.");
			}
			else
			{
				d.directObject().handleEvent(new RealEvent("startup",null,null));
				d.subject().hears("Looping event activated.");
			}
		}


		return true;
	}
}
