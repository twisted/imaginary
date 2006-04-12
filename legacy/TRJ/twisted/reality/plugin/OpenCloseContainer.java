package twisted.reality.plugin;

import twisted.reality.*;

/**
 * This is a generic Open/Close verb for containers. It currently
 * reacts to the following variables on the container:
 *
 *     If there is a boolean "locked" property set to True, the
 *     container will refuse to open, and tell the player it's locked.
 *
 *     If there is a boolean "transparent" property on the object, set
 *     to True, the container's Visible flag will not be toggled when
 *     the container is opened and closed.
 *
 *     If there are "open description" or "closed description" String
 *     properties on the container, they will be made into an
 *     "open/close" description element, and displayed at the
 *     appropriate time. If one or more of the description elements is
 *     missing, the "open/close" element won't be displayed for that
 *     state.
 
 * @author Tenth */

public class OpenCloseContainer extends Verb
{
	public OpenCloseContainer()
	{
		super ("open");
		alias ("close");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing t = d.directObject();
		Player p = d.subject();
		Location l = d.place();
		Location c;

		if (!(t instanceof Location))
		{
			p.hears("You don't think you can open that.");
			return true;
		}
		else
			c = (Location) t;

		if (d.verbString().equals("open"))
		{
			if(c.getBool("locked"))
			{
				Object[] b={p," attempts to open ",c,"."};
				Object[] a={c," appears to be locked."};
				l.tellAll(p,a,b);
			}
			else if(c.areContentsOperable())
			{
				Object[] b={p," fiddles with ",c,"."};
				Object[] a={c," is already open."};
				l.tellAll(p,a,b);
			}
			else
			{
				Object[] a = {"You open ",c,"."};
				Object[] b = {p," opens ",c,"."};
				
				l.tellAll(p,a,b);
				c.setContentsOperable(true);
				if (!(c.getBool("transparent")))
					c.setContentsVisible(true);

				if (c.getString("open description") != null)
					c.putDescriptor("open/close", c.getString("open description"));
				else 
					c.removeDescriptor("open/close");			
			}
		}
		else
		{
			if(!(c.areContentsOperable()))
			{
				Object[] a = {c," is already closed."};
				Object[] b = {p," fiddles with ",c,"."};
				l.tellAll(p,a,b);
			}
			else
			{
				Object[] a = {"You close ",c,"."};
				Object[] b = {p," closes ",c,"."};
				l.tellAll(p,a,b);
				c.setContentsOperable(false);
				if (!(c.getBool("transparent")))
					c.setContentsVisible(false);
				if (c.getString("closed description") != null)
					c.putDescriptor("open/close", c.getString("closed description"));
				else 
					c.removeDescriptor("open/close");
			}
		}
		return true;
	}
}
