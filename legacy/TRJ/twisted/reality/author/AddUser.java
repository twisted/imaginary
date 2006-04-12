package twisted.reality.author;

import twisted.reality.*;

/**
 * Adds a user to the universe.  This creates a classless player - so
 * you'll need to decide whether they should be extended from, say
 * "Class_Player" or "Class_God" or "Class_Human"... or, in your
 * custom map, perhaps "Class_Bleernemebt"?<br>
 *
 * Usage: <code>&gt; adduser <b> &lt;newusername&gt;</b></code>
 *
 * @version 1.1.0, 14 Aug 1999
 * @author Glyph Lefkowitz
 */

public class AddUser extends Verb
{
	public AddUser()
	{
		super("adduser");
		setDefaultPrep("with");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		if (d.subject().isGod())
		{
			new Player(d.place(),d.directString(), "No Description.");
			return true;
		}
		else
		{
			return false;
		}
	}
}
