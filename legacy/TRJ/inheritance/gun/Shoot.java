package inheritance.gun;

import twisted.reality.*;

public class Shoot extends Verb
{
	public Shoot()
	{
		super("shoot");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing target;
		Thing gun=d.indirectObject("with");
		
		if (d.hasDirect())
		{
			target=d.directObject();
		}
		else if (d.hasIndirect("from"))
		{
			target=d.indirectObject("from");
		}
		else
		{
			long aimedTime = gun.getLong("aimed time");
			long now = System.currentTimeMillis();
			
			/* 
			 * Not quite sure what to do here, here's one possibility -- 
			 * if ((now - aimedTime)>Age.OneMinuteMillis) 
			 */
			target=gun.getThing("aimed at");
		}
		
		/* OK, let's do some damage! */
		shoot(gun,d.subject(),target);
		
		return true;
	}
	
	public void shoot(Thing gun, Player p, Thing target) throws RPException
	{
		/* And now, for something completely different!
		 * (note: if target is null, fire randomly. */
	}
}
