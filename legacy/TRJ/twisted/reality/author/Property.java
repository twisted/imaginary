package twisted.reality.author;

import twisted.reality.*;

/**
 * <b>property [string : key] to [DynamicProperty-classname : dproperty]
 * on [local-thing : thing]</b>
 * 
 * <p>Assigns key to the dynamically loaded property dproperty and
 * attaches it to thing.</p>
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Property extends Verb
{
	public Property()
	{
		super("property");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		try
		{
			d.indirectObject("on").putDynProp(d.directString(),d.indirectString("to"));
			d.subject().hears("Dynamic property set.");
		}
		catch (ClassNotFoundException e)
		{
			d.subject().hears("Dynamic Property load failed: " + e);
		}
		return true;
	}
}
