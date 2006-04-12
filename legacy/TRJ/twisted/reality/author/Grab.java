package twisted.reality.author;
import twisted.reality.*;

/**
 * grab [global-thing : thing] 
 * 
 * <p>Teleports thing to the user's current location. Remember to use
 * thing's full global name.</p>
 */

public class Grab extends Verb
{
	public Grab()
	{
		super("grab");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		if(!d.subject().isGod()) return false;
		Thing t = Age.theUniverse().findThing(d.directString());
		if(t!=null)
		{
			if(t instanceof Player)
			{
				Player thep = (Player) t;
				thep.hears("You feel yourself being pulled through space at an incredible speed, and then halted.");
				Object[] phereHear = {"You reach out to ",t," and pull ",Pronoun.obj(t)," into the room."};
				Object[] hereHear = {p," reaches into nowhere and pulls out ",t,", who flies into the room, as if violently tugged."};
				Object[] thereHear = {t," jerks backwards through a hole in space."};
				d.place().tellAll(t, phereHear, hereHear);
				if(t.place() != null)
					t.place().tellAll(t,null, thereHear);
			}
			else
			{
				Object[] pOHereHear = {"You reach out to ",t," and pull ",Pronoun.obj(t)," into the room."};
				Object[] oHereHear = {p," reaches out into nowhere and pulls, and ",t," flies into the room."};
				Object[] oThereHear = {t," jerks backwards through a hole in space."};
				d.place().tellAll(p, pOHereHear,oHereHear);
				if(t.place() != null)
					t.place().tellAll(oThereHear);
			}
			Object[] tLeave = {t," jerks backwards through a hole in space, and vanishes."};
			Object[] tArrive = {t," is pulled through a hole in space by ",d.subject(),"."};
			t.moveTo(d.place(), tLeave, tArrive);
		}
		else
		{
			d.subject().hears("There's no such thing!");
		}
		return true;
	}
}
