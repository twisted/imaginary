package twisted.reality.author;

import twisted.reality.*;

/**
 * Creates a new, blank object, with a new name and no description.<br>
 *
 * Usage: <code>&gt; draw <b>&lt;new object name&gt;</b></code>
 *
 * @version 1.0.0, 12 Jun 1999
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
				Thing th;
				
				// this is a quick hack.  Should integrate some sort
				// of "isReservedWord" checking ... where should this
				// go?
				// --glyph

				if ( d.directString().equals("self") || d.directString().equals("me") || d.directString().equals("here") || d.directString().equals("it") )
				{
					d.subject().hears("I'm sorry.  You can't do that.  Just trust me, you can't.");
				}
				
				th = new Thing(d.place(),d.directString(),Thing.AAn(d.directString())+"rather nondescript "+d.directString()+".");
				
				d.subject().hears
					(
					 "You quickly sketch out a " + d.directString() +
					 " and it appears in front of you."
					 );
				Object[] teb = 
				{d.subject()," moves a pencil through the air in a series of elaborate tracings, and when ",Pronoun.of(d.subject())," finishes, there is ",th.aan(th.name()),
				 d.directString() , " at the tip of the pencil." };
				d.place().tellAll( d.subject(),null,teb );
			}
			else
			{
				d.subject().hears("You attempt to draw something... but the universe pushes back, almost as if there is already something like that, and there's no room for two in one world.");
			}
		}
		else
		{
			d.subject().hears("You attempt to draw with the pencil, but it nearly sears your flesh off your hand as you attempt to do so.  Perhaps you need some other ability in order to use it?");
			d.place().tellEverybodyBut
				(d.subject(),
				 d.subject().name() + " waves a pencil through the air in an attempt to draw something, but quickly appears to be in some pain and stops.");
		}
		
		return true;
	}
}
