package demo;

import twisted.reality.*;

// This is a sarcastic Open/Close verb for the Cash Register Drawer.

public class DrawerOpenClose extends Verb
{
	public DrawerOpenClose()
	{
		super ("open");
		alias ("close");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Location c = (Location) d.directObject();
		Player p = d.subject();
		Location l = d.place();

		if (d.verbString().equals("open"))
		{
			if(c.areContentsOperable())
			{
				Object[] b={p," stares at ",c,"."};
				Object[] a={c," is already open."};
				l.tellAll(p,a,b);
			}
			else
			{
				Object[] a = {"You pull on ",c," but it simply won't open. It's almost like it's locked, or something. Almost EXACTLY as if it were locked, in fact..."};
				Object[] b = {p," grabs ",c," and pulls on it, to no effect."};
				l.tellAll(p,a,b);
			}
		}
		else
		{
			if(!(c.areContentsOperable()))
			{
				Object[] a = {c," is already closed."};
				Object[] b = {p," touches ",c," for a moment."};
				l.tellAll(p,a,b);
			}
			else
			{
				Object[] a = {"You close ",c,"."};
				Object[] b = {p," closes ",c,"."};
				l.tellAll(p,a,b);
				c.setContentsVisible(false);
				c.setContentsOperable(false);
			}
		}
		return true;
	}
}
