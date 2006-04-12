package twisted.reality.author;
import twisted.reality.*;

/**
 * <b>banish [local-thing : thing] </b>
 * 
 * <p>Sets the location of thing to null. This effectively places
 * thing outside the map, where it cannot be reached by normal
 * means. </p>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Banish extends Verb
{
	public Banish()
	{
		super("banish");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing t = d.directObject();
		if(t instanceof Player)
		{
			Player thep = (Player) t;
			Object[] thesub = 
			{"You force ",thep,
			 " out of the bounds of reality, to the void!"};
			Object[] theph = {"You feel sensation draining from your limbs... you've been Banished to a realm of void."};
			Object[] thesil = {thep, " silently vanishes, looking as though ",
							   Pronoun.of(thep)," were trying to scream."};
			d.place().tellAll(d.subject(),thep,
							  thesub,theph,thesil);
			
		}
		else
		{
			Object[] yb = {"You banished ",t," to the endless void."};
			Object[] ee = {twisted.reality.Name.Of(t)," fades out of existance."};
			d.place().tellAll(d.subject(),yb,ee);
		}
		t.place(null);
		return true;
	}
}
