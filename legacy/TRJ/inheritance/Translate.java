package inheritance;

import twisted.reality.*;

/**
 * This verb is for symbols or other static forms of communication
 * that the player can't normally understand. The Thing this verb is
 * enabled on should have a "translates" string property, which, in
 * turn, should be the name of the String property holding the text
 * that the player will be rewarded with for translating the object.
 *
 * This normally takes about 5 seconds to perform... The delay, in
 * seconds, can be specified in a "translation time" Integer property
 * on the translator object.
 *  
 * @author Tenth */

public class Translate extends Verb
{
	public Translate()
	{
		super("translate");
		alias("decipher");
		setDefaultPrep("with");
	}

	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Thing o = d.directObject();
		Thing t = d.verbObject();
		Location l = d.place();
		String language = t.getString("translates");
		String message = o.getString(language);
		int time = t.getInt("translation time");
		if (time == 0)
			time = 5;

		if (language == null)
		{
			Object[] doh = {"On closer inspection, ",t," doesn't seem to be nearly as useful for translation as you expected it to be."};
			p.hears(doh);

			return true;
		}

		if (message == null)
		{
			Object[] doh = {o, " doesn't seem to have any hidden meanings that ",o," could help you understand."};
			p.hears(doh);

			return true;
		}

		Object[] pTrans = {"You begin to examine ",o,", with ",t," as your guide..."};
		Object[] oTrans = {p," examines ",o," closely, referring to ",t," as ",Pronoun.of(p)," does so."};

		l.tellAll(p, pTrans, oTrans);

		p.delay(time);

		d.subject().hears(message);
		
		return true;
	}
}