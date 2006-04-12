package twisted.reality.author;

import twisted.reality.*;

/**
 * Create a new room, given a direction and a new room name . <br>
 *
 * Usage: <code>&gt; dig <b>&lt;direction&gt;</b> to <b>&lt;new room
 * name&gt;</b></code>
 *
 * @version 1.0.1, 12 Aug 1999
 * @author Glyph Lefkowitz
 */

public class Dig extends Verb
{
	public Dig()
	{
		super("dig");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if(d.subject().isGod())
		{
			if(d.hasDirect())
			{
				Room rm=(Room)d.place();
				if( rm.getPortal(d.directString())==null )
				{
					String tempname;
					Room r = new Room(tempname=(d.hasIndirect("to")?d.indirectString("to"):"Plain Room"),Thing.AAn(tempname)+tempname+" looking as if it needs to be described.");
					r.setTheme(d.place().getTheme());
					
					Portal.between(rm,r,d.directString());
					if (rm.place() != null)
						r.place(rm.place());
					d.subject().hears("Exit built.");
				}
				else
				{
					d.subject().hears("That exit's already taken.  Try another one.");
				}
			}
			else d.subject().hears("Please specify a direction to dig in.");
		}
		else
		{
			d.subject().hears("You try, but you don't seem to have the knack, or the strength, or something.");
		}
		
		return true;
	}
}
