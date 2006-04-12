package demo;

import twisted.reality.*;
import twisted.reality.plugin.door.Door;

public class DemoRegisterType extends Verb
{
	public DemoRegisterType()
	{
		super("type");
		alias("enter");
		alias("press");
		setDefaultPrep("on");
	}
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Room room = (Room)d.place();
		Location drawer = (Location) d.verbObject();
		String number = d.directString();
		Integer n;

		if (d.indirectObject("on") != drawer)
			return false;

		try
		{
			n = Integer.valueOf(number);
		}
		catch (NumberFormatException nfe)
		{
			Object[] pHears = {drawer,"'s numeric keypad doesn't seem to be equipped to handle your literary urges."};
			Object[] oHears = {p, " stares thoughtfully at ",drawer,"'s numeric keypad."};
			room.tellAll(p, pHears, oHears);
			return true;
		}

		Object[] pHears = {"You type ",number," on ",drawer,"'s numeric keypad."};
		Object[] oHears = {p, " types a few buttons on ",drawer,"'s keypad."};

		room.tellAll(p, pHears, oHears);

		if (n.intValue() == 1138)
		{
			if (!drawer.areContentsOperable())
			{
				Object[] caChing = {Name.Of(drawer),"'s drawer pops open with a noise that sounds suspiciously like \"Cah-CHING!\""};
				room.tellAll(caChing);
				drawer.setContentsVisible(true);
				drawer.setContentsOperable(true);
				drawer.putDescriptor("open/close", drawer.getString("open description"));
				Score.increase(p,"register",100);
			}
		}
		return true;
	}
}
