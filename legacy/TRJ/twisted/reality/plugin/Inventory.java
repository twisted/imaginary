package twisted.reality.plugin;

import twisted.reality.*;

import java.util.Enumeration;
import java.util.Vector;
import twisted.util.QueueEnumeration;
import twisted.util.FilterEnumeration;

/**
 * Inventory, as in all classic text-adventures, lists the stuff you
 * are carrying. It also lists all of your clothing, including stuff
 * that cannot normally be seen by other people. (You can always look
 * at yourself to make sure you aren't wearing your underwear on the
 * outside of your pants.
 *
 * Usage: <code>&gt; inventory </code>
 *
 * @version 1.0.0, 05 Aug 1999
 * @author Glyph Lefkowitz */

public class Inventory extends Verb
{
	public Inventory()
	{
		super("inventory");
	}
	
	public boolean action(Sentence d)
	{
		QueueEnumeration stuff = new QueueEnumeration();
		QueueEnumeration clothes = new QueueEnumeration();
		Vector c = new Vector();
		Vector s = new Vector();
		boolean hasClothes=false;
		boolean hasStuff=false;

		Enumeration e = d.subject().things();
		while(e.hasMoreElements())
		{
		    Thing thing = (Thing)e.nextElement();
		    if(thing.getBool("clothing worn"))
				clothes.enQueue(thing);
		    else
				stuff.enQueue(thing);
		}
		
		c.addElement("You are wearing ");
		
		while(clothes.hasMoreElements())
		{
			Thing t = (Thing)clothes.nextElement();

			if ( (!(clothes.hasMoreElements())) && hasClothes)
			{
				c.addElement("and ");
			}
			hasClothes=true;
			c.addElement(t);
			if (clothes.hasMoreElements())
			{
				c.addElement(", ");
			}
			else
			{
				c.addElement(".");
			}
		}
		
		s.addElement("You are carrying ");
		final Player plr = d.subject();
		Enumeration estuff = new FilterEnumeration(stuff)
		{
			public boolean filter(Object o)
			{
				Thing t = (Thing) o;
				return ! ( t.isComponent() && t.place() != plr );
			}
		};
		
		while(estuff.hasMoreElements())
		{
			Thing t = (Thing)estuff.nextElement();
			
			if ((!(estuff.hasMoreElements())) && hasStuff)
				s.addElement("and ");
			hasStuff=true;
			s.addElement(t);
			if (t.place() != d.subject())
			{
				s.addElement(" (in ");
				s.addElement(t.place());
				s.addElement(")");
			}
			if (estuff.hasMoreElements())
				s.addElement(", ");
			else
				s.addElement(".");
		}

		if (hasClothes)
			d.subject().hears(c);
		else
			d.subject().hears("You're unclothed.");

		if (hasStuff)
			d.subject().hears(s);
		else
			d.subject().hears("You're empty handed.");
		
		return true;
	}
}
