package divunal.maxwell;

import twisted.reality.*;
/*
 * An enchantment to keep an object in a particular location.
 */
public class AutoReturnGo extends Verb
{
	public AutoReturnGo()
	{
		super("go");
	}

	public boolean action (Sentence d) throws RPException
	{
		Location theplace = d.place();
		Thing specialThing = d.place().getThing("special thing");
		if (specialThing.place() != theplace)
		{
			if (specialThing.place() instanceof Player)
			{
				if (specialThing.place()==d.subject())
				{
					Object[] dsh = {"You trip over something you can't see, and drop ",specialThing," as you try to leave."};
					Object[] esh = {d.subject(), " fumbles and drops ", specialThing, " as ", Pronoun.of(d.subject()), " attempts to leave."};

					d.place().tellAll(d.subject(),dsh,esh);
					Object[] dropit = {d.subject(), " drops ", specialThing,"."};
					specialThing.moveTo(d.place(),dropit);
					return true;
				}
				else return false;
			}

			/* leave this a weak enchantment for now, players can circumvent it
			 * by carrying it off in a box. */

		}
		return false;
	}
}
