package inheritance.gun;
import twisted.reality.*;

/**
 * This is the verb for putting stuff into a clip
 *
 * Sorry, no chopstick instruction manual comments this time...
 *
 * @author Tenth
 */

public class BulletPut extends Verb
{
	public BulletPut()
	{
		super("put");
		alias("load");
	}
	
	public static void load(Location clip, Thing bullet)
	{
		Stack bullets;
		Persistable persistable = clip.getPersistable("bullets");
		if (persistable!=null)
		{
			bullets=(Stack) persistable;
		}
		else
		{
			bullets=new Stack();
		}
		
		bullets.pushThing(bullet);
		
		clip.putPersistable("bullets",bullets);
	}
	
	/* no error reporting -- either there are no bullets left, or this
       isn't realy a clip.  Let's assume the former. */
	
	public static Thing unload(Location clip)
	{
		Stack bullets;
		Thing bullet;
		Persistable persistable = clip.getPersistable("bullets");
		if (persistable!=null)
		{
			bullets=(Stack)persistable;
		}
		else
		{
			bullets=new Stack();
		}
		
		bullet=bullets.popThing();
		
		clip.putPersistable("bullets",bullets);
		return bullet;
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player plr = d.subject();
		Thing bullet = null;
		Thing t = d.directObject();
		Location clip = (Location)d.verbObject();
		
		// if we're trying to load the clip with something
		
		if(d.verbString().equals("load"))
		{
			if (t == clip) 
			{
				bullet = d.indirectObject("with");
			}
			else return false;
		}
		else
		{
			// If we're trying to load something in/into the clip
			
			if (d.hasIndirect("in"))
			{
				if (d.indirectObject("in") == (Thing) clip)
					bullet = t;
				else 
					return false;
			}
		}

		
		// Okay... If we're still here, bullet is definitely what the player
		// has attempted to put into the clip.
		
		// Is the clip accessible?

		if(clip.isComponent() == true)
		{
			plr.hears("You just can't do that right now. But perhaps it would be easier if the clip was accessible...");
			return true;
		}

		// Do you have both the clip and bullet in your hands?

		if(clip.place()!=plr || bullet.place()!=plr)
		{
			plr.hears("You don't have one of those.");
			return true;
		}

		// Is the clip already full?
		
		/* is there ever a time when things other than bullets will be
           in the clip?  I don't think so, but it's possible if we
           check the stack size rather than the clip's element count
           ... */
		
		int bulletsLoaded = clip.thingCount();
		if(bulletsLoaded >= clip.getInt("bullet capacity"))
		{
			Object[] alreadyLoaded = {"There's not enough space left in ",clip," for you to insert ",bullet,"."};
			plr.hears(alreadyLoaded);
			return true;
		}
		
		// Does the bullet fit?

		Room here = (Room) d.place();
		if ((clip.getString("bullet type")).equals(bullet.getString("bullet type")))
		{
			load(clip,bullet);
			Object[] oLoads = {plr," loads ",bullet," into ",clip,"."};
			Object[] pLoads = {"You load ",bullet," into ",clip,"."};
			bullet.moveTo(clip,oLoads);
			here.tellAll(plr, pLoads, oLoads);
		}
		else
		{
			Object[] noMoleste = 
			{"You don't think ",bullet," was meant to be inserted into ",clip,"."};
			Object[] oMoleste = {plr," attempts to force ",bullet," into ",clip,"."};
			here.tellAll(plr, noMoleste, oMoleste);
		}			
	return true;
	}
}
