package twisted.reality.author;

import twisted.reality.*;

/**
 * Make a Thing male.  This also works for players.<br>
 * 
 * Usage: <code>&gt; he <b>&lt;thing name&gt;</b>
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class HeSheIt extends Verb
{
	public HeSheIt()
	{
		super("he");
		alias("she");
		alias("it");
		setDefaultPrep("with");
	}
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;

		Player p = d.subject();
		Thing t = d.directObject();
		String v = d.verbString();
		char c = 'm';

		String ps = "";
		String os = "";
		String ts = "";

		if (p == t)
		{
			if (v.equals("he"))
			{
				ps = "your newfound masculine side";
				os = "masculinity";
			}
			else if (v.equals("she"))
			{
				ps = "your newfound feminine side";
				os = "femininity";
				c = 'f';
			}
			else
			{
				ps = "fleeing Mojo as your gender-specific sexuality melts away";
				os = "gender neutrality";
				c = 'n';
			}

			Object[] pSees = {"You snap your fingers, and you are surrounded by the blinding flash of ",ps,"."};
			Object[] oSees = {p, " snaps ",Pronoun.pos(p) ," fingers, and is enveloped in a blinding flash of ",os,"."};

			d.place().tellAll(p, pSees, oSees);
		}
		else
		{
			if (v.equals("he"))
			{
				ps = "masculine side";
				ts = "a great deal more masculine";
				os = "masculinity";
			}
			else if (v.equals("she"))
			{
				ps = "feminine side";
				ts = "a great deal more feminine";
				os = "femininity";
				c = 'f';
			}
			else
			{
				ps = "gender specific sexuality";
				ts = "strangely neutral of gender";
				os = "gender neutrality";
				c = 'n';
			}

			Object[] pSees = {"You snap your fingers, and there is a blinding flash of light as ",t," rediscovers ",Pronoun.pos(p)," ",ps,"."};
			Object[] tSees = {p, " snaps ", Pronoun.pos(p)," fingers, and there is a blinding flash of light... when your vision clears, you feel a great deal more ",ts,"."};
			Object[] oSees = {p, " snaps ",Pronoun.pos(p)," fingers, and ",t," is enveloped in a blinding flash of ",os,"."};

			d.place().tellAll(p, t, pSees, tSees, oSees);
		}

		t.setGender(c);
		return true;
	}
}
