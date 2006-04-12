package twisted.reality.author;

import twisted.reality.*;

/**
 * <b>int [string : key] on [local-thing : thing] to [string : val]</b>
 *
 * <p>Sets int value <i>key</i> on the thing <i>thing</i> to
 * <i>val</i></p>
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class IntSet extends Verb
{
	public IntSet()
	{
		super("int");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing thing = d.indirectObject("on");
		try
		{
			thing.putInt
				(
				 d.directString(),Integer.parseInt(d.indirectString("to"))
				 );

			Object[] otherhears = {d.subject()," speaks a few words in a language you can't understand, and glowing runes float down from the air and imprint themselves upon ",thing,", then disappear."};
			
			Object[] godhears = {"Int set."};
			
			d.place().tellAll(d.subject(), godhears, otherhears);
		}
		catch (NumberFormatException nfe)
		{
			d.subject().hears("Int not set: That's not an integer...");
		}
		return true;
	} 
}
