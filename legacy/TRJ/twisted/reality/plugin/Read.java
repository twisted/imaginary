package twisted.reality.plugin;

import twisted.reality.*;

/**
 * This verb is for objects which have an additional piece of
 * information that can be read off of it. For especially large pieces
 * of text, consider using TomeRead or one of the other verbs for
 * booklike objects (with multiple turnable "pages").
 *
 * The book should have a "read text" string property, which is the
 * text that the player will see when they attempt to read it.
 * 
 * @author Tenth */

public class Read extends Verb
{
	public Read()
	{
		super("read");
	}

	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Thing o = d.directObject();
 
		if (o == p)
		{
			Object[] pHears = {"You read yourself."};
			Object[] oHears = {p, " reads ", Pronoun.of(p),"self."};
			d.place().tellAll(p, pHears, oHears);
		}
		else
		{
			Object[] pHears = {"You read ", o,"."};
			Object[] fHears = {p, " reads you."};
			Object[] oHears = {p, " reads ", o,"."};
			d.place().tellAll(p, o, pHears, fHears, oHears);
		}
		p.hears(o.getString("read text"));
		return true;
	}
}
