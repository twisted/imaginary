package divunal.damien;

import twisted.reality.*;

/**
 * Deletes an existing thing.<br>
 * 
 * Usage: <code>&gt; erase <b>&lt;thing name&gt;</b></code>
 *
 * @version 1.0, 11 Aug 1999
 * @author Benjamin Scott Hopkins
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
		
		Thing t = d.directObject();
		if(t.name().lastIndexOf("Document") != -1)
		{
			d.subject().hears("What? Erase the Social Contract? I suppose YOU'D prefer a nasty, brutish and SHORT life, eh?");
		}
		else
		{
			Object[] oblt = {t,": obliterated."};
			Object[] takesout = 
			{ d.subject()," takes out a battered parchment and crosses out a few lines. As ", Pronoun.of(d.subject()), " does so, ",
			  t," disappears."};
			t.dispose();
			d.place().tellAll(d.subject(),oblt,takesout);
		}
		
	 return true;
	}
}
