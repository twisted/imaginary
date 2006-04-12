package twisted.reality.author;

import twisted.reality.*;

import java.util.Vector;
import java.util.Enumeration;
import twisted.util.Sort;


/**
 * This outputs the game to a mapfile. <br>
 *
 * Usage: <code>&gt; persist <b>&lt;filename&gt;</b></code>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Persist extends Verb
{
	public Persist()
	{
		super("persist");
		setDefaultPrep("with");
	}
	
	public void everythingBut(Location loc, Player pl, Vector v)
	{
		Enumeration ee = loc.things(true,true);
		while (ee.hasMoreElements())
		{
			Thing t = (Thing) ee.nextElement();
			if (t == pl) continue;
			v.addElement(t);
			/* Object[] xxx = {"( ",t," )"};
			   pl.hears(xxx); */
			if (t instanceof Location)
			{
				everythingBut((Location)t,pl,v);
			}
		}
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		if (d.hasIndirectObject("in"))
		{
			/* this should really be alphabetized, but whatever */
			Thing top = d.indirectObject("in");
			if (top instanceof Location)
			{
				Location topLoc = (Location) top;
				d.subject().hears("Searching...");
				Vector v = new Vector();
				v.addElement(topLoc);
				everythingBut(topLoc,d.subject(), v);
				d.subject().hears("Sorting...");
				v=Sort.quick(v,Sort.ALPHABETICAL);
				d.subject().hears("Saving...");
				Age.theUniverse().persistToFile( d.directString() , v.elements());
				d.subject().hears("Done.");
			}
			else
			{
				d.subject().hears("It's not a location.  Persistence failed.");
			}
		}
		else
		{
			d.subject().hears("Initiating Storage... Please wait, this may take a few moments.");
			Age.theUniverse().persistToFile( d.directString() );
			d.subject().hears("The file has been written.");
		}
		return true;
	}
}
