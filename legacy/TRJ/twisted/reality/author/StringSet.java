package twisted.reality.author;

import twisted.reality.*;

/**
 * <b>string [string : key] on [local-thing : thing] to [string : val]</b>
 *
 * <p>Sets string value <i>key</i> on the thing <i>thing</i> to
 * <i>val</i></p>
 * 
 * <b>string [string : key] on [local-thing : thing]</b>
 *
 * <p>Opens an editor window, allowing you to create a value for string property <i>key</i> on thing <i>thing</i>.
 * <i>val</i></p>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class StringSet extends Verb
{
	public StringSet()
	{
		super("string");
	}

	public void setTell(Player p, Thing t, Location l)
	{
		if (p == t)
		{
			Object[] phears = {"You speak the ascii runes of the property aloud, and they settle onto you."};
			Object[] ohears = {p," speaks a few words in a language you can't understand, and glowing runes float down from the air, imprinting themselves upon ",Pronoun.obj(p),"."};
			l.tellAll(p, phears, ohears);
		}
		else
		{
			Object[] phears = {"You speak the ascii runes of the property aloud, and they settle onto ",t,"."};
			Object[] thears = {p," speaks a few words in a language you can't understand, and glowing runes float down from the air, imprint themselves upon you, and fade away."};
			Object[] ohears = {p," speaks a few words in a language you can't understand, and glowing runes float down from the air, imprint themselves upon ",t,", and fade away."};

			l.tellAll(p, t, phears, thears, ohears);
		}
	}

	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		if (!p.isGod()) return false;
		Thing thing = d.indirectObject("on");
		Location l = d.place();

		if (d.hasIndirect("to"))
		{
			thing.putString(d.directString(),d.indirectString("to"));
			setTell(p, thing, l);
		}
		else
		{
			Object[] phear = {"You begin to contemplate the value of ",d.directString(),"..."};
			if (p == thing)
			{
				Object[] ohear = {p, " speaks a few halting syllables in a language you can't understand, and glowing runes begin to appear and shift over ", Pronoun.obj(p),"..."};
				l.tellAll(p, phear, ohear);
			}
			else
			{
				Object[] thear = {p, " speaks a few halting syllables in a language you can't understand, and glowing runes begin to fade in and shift over your body..."};
				Object[] ohear = {p, " speaks a few halting syllables in a language you can't understand, and glowing runes begin to fade in and shift over ", thing,"..."};
				l.tellAll(p, thing, phear, thear, ohear);
			}
			String propString;
			p.requestResponse
				(new StringPropProcessor
					 (thing,
					  p,
					  d.directString(),
					  null),
				 " Contents of String Property " +
				 d.directString() +
				 " on " + thing.NAME() +
				 ".",
				 thing.getString(d.directString())
				 );
		}
		return true;
	}
}
