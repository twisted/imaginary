package divunal.damien;

import twisted.reality.*;

/**
 * Creates a new, blank object, with a new name and no description.<br>
 *
 * Usage: <code>&gt; draw <b>&lt;new object name&gt;</b></code>
 *
 * @version 0.99.1, 15 Jun 1998
 * @author Glyph Lefkowitz
 */

public class Draw extends Verb
{
	public Draw()
	{
		super("draw");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if(d.subject().isGod())
		{
			if(Age.theUniverse().findThing(d.directString())==null)
			{
				Thing th = new Thing(d.place(),d.directString(),"A white box.");
				Object[] addendum = 
				{ "You add an adendum covering the ", d.directString(),
				  " to the Social Contract."  };
				Object[] paperwhip =
				{ Name.Of(d.subject()), " whips out a somewhat battered piece of paper. ",
				  Pronoun.of(d.subject()),
				  " scratches out a few lines, adds in a few more, and when ",Pronoun.of(d.subject()),
				  " is done, a ",
				  d.directString(),
				  " becomes a part of the current reality."};
				
				d.place().tellAll(d.subject(),addendum,paperwhip);
			}
			else
			{
				d.subject().hears("That is already covered in section 451-A, sub-paragraph H. While redundency is always sought after, there is no need for another "+ d.directString());
			}
		}
		else
		{
			Object[] apathy = {"You attempt to edit the Social Contract, but it nearly sears your flesh off your hand as you attempt to do so.  Perhaps you need some other ability in order to use it?"};
			
			Object[] agony = {Name.Of(d.subject()), "  agonizes over a battered piece of parchment in an attempt to change something, but appears to be in some pain and stops."};
			
			d.place().tellAll(d.subject(),apathy,agony);
		}
		
		return true;
	}
}
