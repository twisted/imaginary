package twisted.reality.author;

import twisted.reality.*;

/**
 * Extend lets you change the superclass of any given object.  Using
 * extension (subclassing) you can save lots of memory by just having
 * one parent object (like 'Class_Sword') and lots of child-objects (kyle's
 * sword, glyph's sword, james's sword...). <br>
 *
 * Usage: <code>&gt; extend <b>&lt;subthing-name&gt;</b> from
 * <b>&lt;superthing-name&gt;</b></code>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Extend extends Verb
{
	public Extend()
	{
		super("extend");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing s = Age.theUniverse().findThing(d.indirectString("from"));
		if (s == null)
		{
			if (!d.indirectString("from").equals("null"))
			{
				d.subject().hears("Can't find thing " + d.indirectString("from"));
				return true;
			}
		}
		
		if(d.directObject().setSuperClass(s))
		{
			d.subject().hears("Successful subclassage.");
		}
		else
		{
			d.subject().hears("Something went Horribly Wrong.  Circular dependancy or other BAD error. (Read the log, please.)");
		}
		return true;
	}
}
