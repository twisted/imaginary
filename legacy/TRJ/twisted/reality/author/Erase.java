package twisted.reality.author;

import twisted.reality.*;

/**
 * Deletes an existing thing.<br>
 * 
 * Usage: <code>&gt; erase <b>&lt;thing name&gt;</b></code>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Erase extends Verb
{
	public Erase()
	{
		super("erase");
		setDefaultPrep("with");
	}
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing t = d.directObject();
		if(t == d.verbObject())
		{
			d.subject().hears("Yow! the pencil doesn't bend like that.");
		}
		else
		{
			Object[] oblt = {t, ": obliterated."};
			Object[] ertc = {d.subject().name(),
							 " touches an eraser lightly to ",
							 t, " and ", Pronoun.of(t)," disappears."};
			d.place().tellAll(d.subject(),oblt,ertc);
			t.dispose();
		}
		
		return true;
	}
}
