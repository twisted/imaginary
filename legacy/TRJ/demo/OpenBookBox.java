package demo;

import twisted.reality.*;

// This is for hollowed-out books used as boxes; Attempting to read
// them acts as Open, and you can close them again afterwards.

public class OpenBookBox extends Verb
{
	public OpenBookBox()
	{
		super ("open");
		alias ("read");
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
			p.hears("There's something very wrong with this object, but you're not quite sure what.");
			return true;
		}
		else
		{
			c = (Location) t;
		}

		Object[] fiddler = {Name.Of(p)," fiddles with ",c,"."};
		if (!(d.verbString().equals("close")))
		{
			if(c.areContentsOperable())
			{
				Object[] isOpen ={Name.Of(c)," is already open."};
				d.place().tellAll(p,isOpen,fiddler);
				p.setFocus(c);
			}
			else
			{
				Object[] pagesCutOut={
					"The center of the pages in ",c,
					" seem to have been cut out, forming a small box."
				};
				Object[] itOpens={
					p," opens ",c
				};
				
				l.tellAll(p,pagesCutOut,itOpens);
				
				c.setContentsVisible(true);
				c.setContentsOperable(true);
				
				c.putDescriptor("opened", "It is open, revealing that the center of each page has been removed, making it useless as a book but quite functional as a container.");
			}
		}
		else
		{
			if(!(c.areContentsOperable()))
			{
				Object[] isClosed = {Name.Of(c)," is already closed."};
				d.place().tellAll(p,isClosed,fiddler);
				
			}
			else
			{
				Object[] uClose = {"You close ",c,"."};
				Object[] closes = {Name.Of(p)," closes ",c,"."};
				
				d.place().tellAll(p,uClose,closes);
				
				c.setBroadcast(false);
				c.removeDescriptor("opened");
				c.setContentsOperable(false);
				c.setContentsVisible(false);
			}
		}
		return true;
	}
}
