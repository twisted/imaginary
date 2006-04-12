package inheritance.gun;

import twisted.reality.*;

/*
 * Lucky lucky good clip
 * 
 * @author Glyph
 */

public class BulletGet extends Verb
{
	public BulletGet()
	{
		super("get");
		alias("take");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		// Are they just trying to pick up the clip?

		if (d.verbObject() == d.directObject())
			return false;

		Location clip = (Location) d.verbObject();
		Thing bullet = d.directObject();
		Player plr = d.subject();

		// Is the clip accessible?

		if(clip.isComponent() == true)
		{
			plr.hears("You just can't do that right now. But perhaps it would be easier if the clip was accessible...");
			return true;
		}

		if (bullet.place()==clip)
		{
			Thing otherBullet = BulletPut.unload(clip);
			
			if (otherBullet==bullet)
			{
				Object[] xxx={"You take ",bullet,"."};
				plr.hears(xxx);
				/*It must be your lucky day!*/
			}
			else
			{
				Object[] xxx={"You can't reach ",
							  bullet,", so you pop ",
							  otherBullet,
							  " out of the clip instead."};
				plr.hears(xxx);
				/*You're not so lucky*/
			}
			Object[] obt={plr," pops ",otherBullet," out of the clip."};
			otherBullet.moveTo(plr,obt);
			return true;
		}
		/* I don't know where you found this verb, but you weren't
           trying to take something out of the clip. */
		/* (now you can pick up anything) */
		else return false;
	}
}
