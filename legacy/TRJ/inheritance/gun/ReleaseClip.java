package inheritance.gun;
import twisted.reality.*;

/**
 * This is the verb for releasing the Clip
 * 
 * Whoop, whoop...
 *
 * @author Tenth
 */

public class ReleaseClip extends Verb
{
	public ReleaseClip()
	{
		super("release");
		alias("remove");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player plr = d.subject();
		Thing clip = d.directObject();
		
		if (clip.isComponent() == false)
		{
			if(!(clip.place().place() == plr))
			{
				return false;
			}
		}

		Location gun = clip.place();
		if (!(gun.getThing("loaded with").equals(clip)))
		{
			return false;
		}

		if(gun.place() == plr)
		{
			clip.setComponent(false);
			gun.removeProp("loaded with");
			clip.place(plr);
			Object[] oUnLoads = {plr," removes ",clip," from ",gun,"."};
			Object[] pUnLoads = 
			   {"You release ",clip," and remove it from ",gun,"."};
			d.place().tellAll(plr, pUnLoads, oUnLoads);
		}
		else
		{
			plr.hears("You don't have one of those.");
		}
		return true;
	}
}
