package twisted.reality.plugin;

import twisted.reality.*;
import java.util.Enumeration;
import twisted.util.LinkedList;

/**
 * Gets an object you don't got, that's available to you.
 *
 * Usage: <code>&gt; take <b>&lt;thing&gt;</b></code>
 *
 * @version 1.0.0, 15 Jun 1998
 * @author Glyph Lefkowitz
 */

public class Take extends Verb
{
	public Take()
	{
		super("take");
		alias("get");
	}

	public boolean action(Sentence d) throws RPException
	{
		String s;
		Player plr = d.subject();
		Thing t;
		Location loc = null;
		
		/*
		 * Let's find out what exactly it is the player wants to get.
		 */
		
		/*
		 * Are they trying to get something from something else?
		 */
		
		if(d.hasIndirect("from"))
		{
			try
			{
				/*
				 * Get the location they're talking about.
				 */
				
				loc = (Location)d.indirectObject("from");
			}
			
			/*
			 * It's not a location?  Well, this is an error, so flag
			 * it as such and note that we don't know what to do in
			 * this situation.
			 */
			
			catch(ClassCastException e){ return false; }
		}
		
		/*
		 * Using the location which we either obtained or didn't,
		 * let's figure out what object the player's referring to.
		 */
		
		try
		{
			if(loc == null)
				t = d.directObject();
			else
			{
				t = loc.findThing(d.directString(), d.subject());
				if (t==null)
				{
					throw new NoSuchThingException(d.directString());
				}
			}
		}
		
		/*
		 * If there is an ambiguity, resolve it by looking for objects
		 * which I am not already carrying.
		 */
		
		catch(AmbiguousException ae)
		{
			t=TRUtils.reduceAmbiguity(ae,plr,new TRUtils.Not(new TRUtils.IsIn(plr)));
		}
		
		if(t.place()==plr)
		{
			plr.hears("You're already holding that.");
		}
		else
		{
			/*
			 * Now that we know what it is that we're supposed to be
			 * taking, exactly, let's see if we can take it.
			 */
			
			/* If it's a player, we can't, since that wouldn't be polite. */
			if (t instanceof Player)
			{
				/* we're not flexible enough if it's us */
				if (t == plr)
				{
					char gndr = plr.getGenderTo(plr);
					switch(gndr)
					{
					case 'f':
						s = "girl";
						break;
					case 'm':
						s = "boy";
						break;
					default:
						s = "thing";
						break;
					}
					
					Object[] temp = 
					{
						"Nice try, pretzel ",
						s,
						", but you lack the flexibility, strength, and gravity-defying powers you'd need to accomplish that."
					};
					plr.hears(temp);
				}
				/* otherwise we're not rude enough */
				else
				{
					plr.hears("That would be very, very rude.");
				}
			}
			else
			{
				/* it would also be rude to take something someone else was carrying */
				if(isLocatedInOtherPlayer(t,plr))
				{
					Object[] txt = {"I don't think ",loc," would like that very much."};
					plr.hears(txt);
					return true;
				}
				
				
				Object[] tmps={plr," takes ",t,"."};
				switch (canTake(plr,t))
				{
				case CAN_TAKE:
					if(t.moveTo(plr,tmps,tmps))
						plr.hears(t.nameTo(plr) + ": taken.");
					else plr.hears("You can't take that.");
					break;
				case TOO_HEAVY:
					plr.hears(t.nameTo(plr)+ ": not taken, too heavy.");
					break;
				case TOO_UNWEILDY:
					plr.hears(t.nameTo(plr)+": not taken, you're carrying too many things already.");
					break;
				case TOO_BOTH:
					plr.hears(t.nameTo(plr)+": not taken, you would need to unload first.");
					break;
				case TOO_STUPID:
				default:
					plr.hears(t.nameTo(plr)+": not taken, that would be silly.");
				}
			}
		}
		return true;
	}
	
	public static final int CAN_TAKE=1;
	public static final int DEFAULT_CHECK=0;
	public static final int TOO_HEAVY=-1;
	public static final int TOO_UNWEILDY=-2;
	public static final int TOO_BOTH=-3;
	public static final int TOO_STUPID=-4;
	
	public static final boolean isLocatedInOtherPlayer(Thing t, Player p)
	{
		Location l = t.place();
		while (l != null)
		{
			if (l instanceof Player && l != p)
				return true;
			l=l.place();
		}
		return false;
	}

	/**
	 * This determines, based on weight and classification
	 * constraints, whether a player can take an object.  This does
	 * not take into account `politeness' factor, so this is
	 * acceptible for determining whether you can steal an object or
	 * not.
	 */
	
	public static final int canTake(Player p, Thing t)
	{
		int i = p.getInt("canTake",t);
		if (i!=DEFAULT_CHECK) return i;
		return defaultCanTake(p, t);
	}
	
	/**
	 * This performs the default is it too heavy / does it weigh too
	 * much check.  It is: max weight is 1, max weildiness is 1.
	 * Objects which are component to the player are not calculated.
	 */
	
	public static final int defaultCanTake(Player p, Thing t)
	{
		float weight = t.getFloat("weight",p);
		float weildiness = t.getFloat("weildiness",p);
		
		float currweild = 0;
		float currweight = 0;
		
		Enumeration e = p.things(true,true);
		
		while(e.hasMoreElements())
		{
			Thing o = (Thing) e.nextElement();
			
			float gh = o.getFloat("weight",p);
			float ld = o.getFloat("weildiness",p);
			
			if (gh == 0) gh = (float)0.05;
			
			if (ld == 0) ld = (float)0.1;
			
			if (o.isComponent()) { ld /= 10; }
			
			currweild += ld;
			currweight += gh;
		}
		if ( (currweild+weildiness) > 1)
			if ((currweight+weight) < 1)
				return TOO_UNWEILDY;
			else return TOO_BOTH;
		else if ((currweight + weight) > 1)
			return TOO_HEAVY;
		else
			return CAN_TAKE;
	}
}
