package inheritance.gun;
import twisted.reality.*;

/**
 * This is the verb for pressing the Switch
 *
 * @author Tenth
 */

public class ReleasePress extends Verb
{
	public ReleasePress()
	{
		super("press");
		alias("push");
		alias("flip");
		alias("turn");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player plr = d.subject();
		Thing rswitch = d.directObject();
		Location gun = rswitch.place();
		Thing clip = gun.getThing("loaded with");

		if (gun.place() != plr)
		{
			plr.hears("You don't have one of those.");
			return true;
		}

		if (clip == null)
		{
			plr.hears("You press the release, but nothing happens.");
			return true;
		}

		clip.setComponent(false);
		gun.removeProp("loaded with");
		clip.place(plr);
		Object[] oUnLoads = {plr," removes ",clip," from ",gun,"."};
		Object[] pUnLoads = 
		   {"You release ",clip," and remove it from ",gun,"."};
		d.place().tellAll(plr, pUnLoads, oUnLoads);

		return true;
	}
}
