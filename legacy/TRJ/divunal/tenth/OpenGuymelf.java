package divunal.tenth;

import twisted.reality.*;

// This is a generic Open/Close verb for
// containers.

public class OpenGuymelf extends Verb
{
	public OpenGuymelf()
	{
		super ("open");
		alias ("close");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing t = d.directObject();
		Player p = d.subject();
		Location l = p.place();
		Location v = (Location) t;
		Location r = v.place();

		if (d.verbString().equals("open"))
		{
			if (l == v)
			{
				if(v.areContentsOperable())
				{
					p.hears("The armor is already open.");
				}
				else
				{
					Object[] pSees = {"You pull the \"Release\" valve, and the chest plates of the armor slide open, letting in some much needed fresh air."};
					Object[] oSees = {"The chest plates of the armor split apart, revealing ",p," sitting inside of it."};
					v.setBroadcast(true);
					v.setContentsVisible(true);
					v.setContentsOperable(true);
					r.tellAll(p, pSees, oSees);
				}
			}
			else
			{
				if(v.areContentsOperable())
				{
					p.hears("The armor is already open.");
				}
				else p.hears("You don't see any way to open it.");
			}
		}
		else
		{
			if (l == v)
			{
				if(!(v.isBroadcast()))
				{
					p.hears("The armor is already closed.");
				}
				else
				{
					Object[] pHears = {"You pull the armor closed around you."};
					Object[] oHears = {p," pulls on something inside the armor, and it closes around ",Pronoun.obj(p),"."};
					r.tellAll(p,pHears,oHears);
					v.setContentsVisible(false);
					v.setBroadcast(false);
					v.setContentsOperable(false);
				}
			}
			else if(!(v.isBroadcast()))
			{
				Object[] pDumb = {"The armor is already closed."};
				Object[] oDumb = {p," stares at the armor for a moment."};
				r.tellAll(p,pDumb,oDumb);
			}
			else
			{
				Object[] pClose = {"There is a faint hissing sound as you begin to push the chest plate, and the armor folds itself shut."};
				Object[] oClose = {p," pushes on one of the open chest plates, and the armor closes itself."};
				r.tellAll(p, pClose, oClose);
				v.setContentsVisible(false);
				v.setBroadcast(false);
				v.setContentsOperable(false);
			}
		}	
		return true;
	} //Action
} //Class
