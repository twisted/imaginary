package inheritance.gun;
import twisted.reality.*;
import inheritance.gun.RackSlide;
/**
 * This verb for putting stuff into gun
 * 
 * Now you can pick up anything.
 *
 * @author Tenth
 */

public class GunPut extends Verb
{
	public GunPut()
	{
		super("put");
		alias("load");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player plr = d.subject();
		Thing clip = null;

		if (d.hasDirectObject())
		{
			Thing t = d.directObject();
			Location gun = (Location)d.verbObject();

			// if we're trying to load the gun with something

			if(d.verbString().equals("load"))
			{
				if (t == gun) 
				{
					clip = d.indirectObject("with");				
				}
				else
					return false;
			}
			else
			{
				// If we're trying to load something in/into the gun

				if (d.hasIndirect("in"))
				{
					if (d.indirectObject("in") == (Thing) gun)
						clip = t;
					else 
						return false;
				}
			}

			// Okay... If we're still here, clip is definitely what the player
			// has attempted to put into the gun.

			if(gun.place()!=plr || clip.place()!=plr)
			{
				plr.hears("You don't have one of those.");
				return true;
			}

			if(!(gun.getThing("loaded with") == null))
			{
				Object[] alreadyLoaded = {"There's not enough space left in ",gun," for you to insert ",clip,"."};
				plr.hears(alreadyLoaded);
				return true;
			}

			Location here = d.place();

			if ((gun.getString("clip type")).equals(clip.getString("clip type")))
			{
				gun.putThing("loaded with", clip);
				clip.place(gun);
				clip.setComponent(true);
				Object[] oLoads = {plr," slides ",clip," into ",gun,", and it snaps into place with a faint clicking sound."};
				Object[] pLoads = {"You slide ",clip," into ",gun,", and it snaps into place with a faint clicking sound."};
				here.tellAll(plr, pLoads, oLoads);
				RackSlide.UnLockSlide(gun);
			}
			else
			{
				Object[] noMoleste = 
				{"You don't think ",clip," was meant to be inserted into ",gun,"."};
				Object[] oMoleste = {plr," struggles with ",clip," for a few seconds, attempting to jam it into ",gun,"."};
				here.tellAll(plr, noMoleste, oMoleste);
			}			
		}
		else
		{
			plr.hears("You don't have one of those.");	
		}
		return true;
	}
}
