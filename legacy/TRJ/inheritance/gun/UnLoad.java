package inheritance.gun;
import twisted.reality.*;

/**
 * This is a verb for unloading the Gun
 *
 * @author Tenth
 */

public class UnLoad extends Verb
{
	public UnLoad()
	{
		super("unload");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player plr = d.subject();
		Location gun = (Location)d.directObject();
		Thing clip = gun.getThing("loaded with");
		
		if(clip == null)
		{
			Object[] notLoaded = {"There's nothing to unload from ",gun,"."};
			plr.hears(notLoaded);
			return true;
		}
		
		Room here = (Room) d.place();

		clip.setComponent(false);		
		gun.removeProp("loaded with");
		clip.place(plr);
		Object[] oUnLoads = {plr," removes ",clip," from ",gun,"."};
		Object[] pUnLoads = {"You release ",clip," and remove it from ",gun,"."};
		here.tellAll(plr, pUnLoads, oUnLoads);
		
		return true;
	}
}

