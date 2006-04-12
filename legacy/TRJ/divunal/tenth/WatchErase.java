package divunal.tenth;

import twisted.reality.*;

/**
 * Deletes an existing thing.<br>
 * 
 * Usage: <code>&gt; erase <b>&lt;thing name&gt;</b></code>
 *
 * @version 1.0, 30 Jul 1999
 * @author Glyph Lefkowitz
 */

public class WatchErase extends Verb
{
	public WatchErase()
	{
		super("erase");
		setDefaultPrep("with");
	}
	public boolean action(Sentence d) throws RPException
	{
		Thing t = d.directObject();
		Object[] subj = {"You release the stem, and "
						 ,t," collapses into nothingness."};
		
		Object[] others = {d.subject()
						   , " casually adjusts "
						   , Name.of(d.withObject(),d.subject())
						   , ", and "
						   , t
						   , " collapses into a complex series of lines which scatter into nothingness."
						   };
		d.place().tellAll(d.subject(),subj,others);
		
		if(t == d.verbObject() || t == d.subject())
		{
			d.subject().hears("You get the strange, nagging feeling that you have done something very foolish.");
		}
		
		if (!(d.subject().isGod()))
			return false;

		t.dispose();
		return true;
	}
}
