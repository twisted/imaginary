package divunal.tenth;

import twisted.reality.*;

// This is a generic Open/Close verb for
// containers.

public class EnterGuymelf extends Verb
{
	public EnterGuymelf()
	{
		super ("enter");
		alias ("board");
		alias ("exit");
		alias ("leave");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing t = d.directObject();
		Player p = d.subject();
		Location l = d.place();
		Location v = (Location) t;
		Location room = t.place();
		String verb = d.verbString();

		if (verb.equals("enter") || verb.equals("board"))
		{
			if (d.place() == v)
			{
				p.hears("You're already inside the armor...");
			}
			else
			{
				if (v.areContentsOperable() == false )
				{
					Object[] othersHear = {p," tugs at the chest plate of the armor."};
					Object[] playerHears = {"You can't see any way to get inside of it."};
					room.tellAll(p, playerHears, othersHear);
				}
				else
				{
					Object[] othersSee = {p, " climbs inside of the armor's open chest, and it closes around ",Pronoun.obj(p)," with a faint hissing sound."};
					Object[] playerSees = {"You climb into the armor's open chest, and sit back as it closes tightly around you."};
					Object[] vLeave = {p, " climbs into the armor."};
					Object[] vArrive = {p, " steps inside."};
					v.setContentsOperable(false);
					v.setContentsVisible(false);
					v.setBroadcast(false);
					room.tellAll(p, playerSees, othersSee);
					p.moveTo(v, vLeave, vArrive);
				}
			}
		}
		else
		{
			if (p.place() == v)
			{
				Object[] oLeave = {p," climbs out."};
				Object[] oArrive = {p, " climbs out of the armor."};
				p.moveTo(room, oLeave, oArrive);

				if (v.areContentsOperable() == false)
				{
					Object[] othersNotice = {"The chest plates of the armor split apart, and ",p," climbs out of it."};
					Object[] playerNotices = {"The chest plates split open, and you step out into the fresh, open air outside the suit."};
					room.tellAll(p, playerNotices, othersNotice);
				}
				else
				{
					Object[] pNoOpen = {"You climb out of the armor."};
					Object[] oNoOpen = {p," climbs out of the armor's open chest."};
					room.tellAll(p, pNoOpen, oNoOpen);
				}
				v.setContentsOperable(true);
				v.setContentsVisible(true);
				v.setBroadcast(true);
			}
			else
			{
				p.hears("You'd have to be in the suit to get out of it, now, wouldn't you?");
			}
		}
		return true;
	}
}
