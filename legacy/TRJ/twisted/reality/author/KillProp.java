package twisted.reality.author;

import twisted.reality.*;
/**
 * <b>killprop [string : key] on [local-thing : thing]
 * 
 * <p>Removes the property 'key' from the thing 'thing'.</p>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */
public class KillProp extends Verb
{
	public KillProp()
	{
		super ("killprop");
	}
	
	/**
	 * Destroy a property on an object.
	 */
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		String propname = d.directString();
		Thing thing = d.indirectObject("on");
		
		if (thing.hasProp(propname))
		{
			thing.removeProp(propname);
			d.subject().hears("Property eliminated.");
		}
		else
		{
			d.subject().hears(thing.NAME()+" bears no such property.");
		}
		return true;
	}
}
