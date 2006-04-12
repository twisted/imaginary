package twisted.reality.author;
import twisted.reality.*;

/**
 * toss [global-thing : thing] to [global-thing : location] 
 * 
 * <p>Teleports thing to location. Remember to use full global names.
 * Currently, to prevent oddness, you can only put players into rooms.</p>
 *
 * David Sturgis  19 Aug 1999
 */

public class Toss extends Verb
{
	public Toss()
	{
		super("toss");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Room here = (Room) d.place();
		if(!d.subject().isGod()) return false;
		Thing obj = d.directObject();
		Thing r=Age.theUniverse().findThing(d.indirectString("to"));

		if (r != null)
		{
			if (r instanceof Location)
			{
				Location place = (Location) r;

				Object[] pmLeave = {twisted.reality.Name.Of(obj), " is thrown through a hole in space by ",p,"."};
				Object[] pmArrive = {twisted.reality.Name.Of(obj), " pops out of an invisible hole in the air."};

				if (obj instanceof Player)
				{
					if (obj == p)
					{
						p.hears("You pervert.");
						return true;
					}
				
					Object[] othersSee = {p, " gives ",obj," a good shove, and ", Pronoun.of(obj)," stumbles backwards through an invisible hole in reality."};
					Object[] playerSees = {"You give ",obj," a good shove, and ",Pronoun.of(obj)," stumbles backwards through a hole in space and time."};
					Object[] tossedSees = {p, " gives ",obj," a good shove, and ", Pronoun.of(obj)," stumbles backwards through an invisible hole in reality."};
					here.tellAll(p,obj,playerSees, tossedSees, othersSee);
					place.tellAll(pmArrive);
					obj.moveTo(place, pmLeave, pmArrive);
				}			
				else
				{
					Object[] playeroSees = {"You grab ",obj," and toss it through a hole in space."};
					Object[] othersoSee = {p, " grabs ", obj, " and tosses it through a hole in the air."};
					here.tellAll(p, playeroSees, othersoSee);
					place.tellAll(pmArrive);
					obj.moveTo(place, pmLeave, pmArrive);
				}
			}
			else p.hears("That would be cruel and destructive.");
		}
		else p.hears("Wait... You want to toss what where?");
		
		return true;
	}
}
