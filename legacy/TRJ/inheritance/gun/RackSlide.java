package inheritance.gun;

import twisted.reality.*;
import inheritance.gun.BulletPut;

/**
 * This is the verb for working/cocking/
 * racking the slide/action
 *
 * @author Tenth
 */

public class RackSlide extends Verb
{
	public RackSlide()
	{
		super("rack");
		alias("work");
		alias("cock");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Thing slide = d.verbObject();
		Location gun = slide.place();
		Location clip = (Location) gun.getThing("loaded with");
		Location chamber = (Location) gun.getThing("chamber");
		boolean locked = gun.getBool("slide lock");
		Location l = d.place();

		if (locked == true)
		{
			p.hears("The slide is locked back already... Perhaps the gun needs to be loaded first?");
			return true;
		}
		if (chamber.thingCount() == 0)
		{
			Object[] pRackLock = {"You pull back the slide, and it remains locked in place."};
			Object[] oRackLock = {p, " cocks ", gun, ", but it stays locked back."};

			if (clip != null)
			{
				if (clip.thingCount() > 0)
				{
					Object[] pRacks = {"You rack the slide, and the gun produces a satisfying click."};
					Object[] oRacks = {p, " cocks ", gun, "."};
					Thing bullet = BulletPut.unload(clip);
					bullet.place(null);
					bullet.moveTo(chamber, null);
					l.tellAll(p, pRacks, oRacks);
				}
				else
				{
					l.tellAll(p, pRackLock, oRackLock);
					LockSlide(gun);
				}
			}
			else
			{
				l.tellAll(p, pRackLock, oRackLock);
				LockSlide(gun);
			}
		}
		else
		{
			Thing bullet = chamber.findThing("bullet", gun);
			Object[] pEjects = {"As you rack the slide, ",bullet," is ejected from the port and clatters to the floor."};
			Object[] oEjects = {p, " cocks ", gun, ", and ",bullet," tumbles from the side and clatters to the floor."};
			Object[] bMove = {bullet, " is ejected from the side of ",gun,"."};
			bullet.moveTo(p.place(), bMove);
			l.tellAll(p, pEjects, oEjects);

			Object[] alocks = {"The ",gun,"'s slide has locked back."};

			if (clip != null)
			{
				if (clip.thingCount() > 0)
				{
					bullet = BulletPut.unload(clip);
					bullet.place(chamber);
				}
				else
				{
					LockSlide(gun);
					l.tellAll(alocks);
				}
			}
			else
			{
				LockSlide(gun);
				l.tellAll(alocks);
			}
		}
		return true;
	}

	public static void LockSlide(Thing gun)
	{
		gun.putBool("slide lock", true);
		gun.putDescriptor("slide locked", "The slide is pushed all the way back, and appears to be locked in place.");
	}
	public static void UnLockSlide(Thing gun)
	{
		gun.putBool("slide lock", false);
		gun.removeDescriptor("slide locked");
	}
}
