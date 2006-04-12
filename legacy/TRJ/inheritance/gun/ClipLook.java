package inheritance.gun;

import twisted.reality.*;

// This verb intercepts any attempts to look at the
// the clip, and fails them if it's in the gun.

public class ClipLook extends Verb
{
	public ClipLook()
	{
		super ("look");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Location clip = (Location) d.verbObject();
		Location gun = clip.place();

		// Is the clip in the gun?

		if (clip.isComponent())
		{
			// Are they referring directly (or indirectly) to the clip?
			
			if (d.directObject() == clip || d.indirectObject("at") == clip)
			{
				Object[] noWay = {"You'll have to take it out of ",gun," first."};
				p.hears(noWay);
				return true;
			}
		}
		return false;
	}
}
