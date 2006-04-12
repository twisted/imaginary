package twisted.reality.author;

import twisted.reality.*;

/**
 * <b>float [string : key] on [local-thing : thing] to [string : val]</b>
 *
 * <p>Sets float value <i>key</i> on the thing <i>thing</i> to
 * <i>val</i></p>
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class FloatSet extends Verb
{
	public FloatSet()
	{
		super("float");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing thing = d.indirectObject("on");
		try
		{
			thing.putFloat
				(
				 d.directString(),
				 Float.valueOf(d.indirectString("to")).
				 floatValue()
				 );

			Object[] otherhears = {d.subject()," speaks a few words in a language you can't understand, and glowing runes float down from the air and imprint themselves upon ",thing,", then disappear."};
			
			Object[] godhears = {"Float set."};
			
			d.place().tellAll(d.subject(), godhears, otherhears);
		}
		catch (NumberFormatException nfe)
		{
			d.subject().hears("Float not set: That's not a number...");
		}
		return true;
	} 
}
