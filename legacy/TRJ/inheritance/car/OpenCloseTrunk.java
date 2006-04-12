package inheritance.car;

import twisted.reality.*;

// This is a generic Open/Close verb for
// containers.

public class OpenCloseTrunk extends Verb
{
	public OpenCloseTrunk()
	{
		super ("open");
		alias ("close");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing t = d.directObject();
		Player p = d.subject();
		Location trunk = (Location) d.verbObject();
		String descElement;
		Location l = d.place();
		Object[] oFiddle= {p," fiddles with ",trunk,"."};		

		if (t != trunk)
		{
			return false;
		}

		if (p.place() == trunk.place())
		{
			p.hears("You'll have to get out of the car first.");
			return true;
		}

		if (d.verbString().equals("open"))
		{
			if(trunk.areContentsOperable())
			{
				Object[] a={trunk," is already open."};
				l.tellAll(p,a,oFiddle);
			}
			else
			{
				Object[] a = {"You open ",trunk,"."};
				Object[] b = {p," opens ",trunk,"."};
				
				l.tellAll(p,a,b);
				trunk.setContentsOperable(true);
				trunk.setContentsVisible(true);
				descElement = trunk.getString("open description");
				trunk.describe(descElement);
			}
		}
		else
		{
			if(trunk.areContentsOperable())
			{
				Object[] a = {"You close ",trunk,"."};
				Object[] b = {p," closes ",trunk,"."};
				l.tellAll(p,a,b);
				trunk.setContentsVisible(false);
				trunk.setContentsOperable(false);
				descElement = trunk.getString("closed description");
				trunk.describe(descElement);
			}
			else
			{
				Object[] a = {trunk," is already closed."};
				l.tellAll(p,a,oFiddle);
			}
		}
		return true;
	}
}
