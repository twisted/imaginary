package demo;

import twisted.reality.*;

/**
 * This is the disturbing verb for the drinking fountain.
 *
 * @author Tenth */

public class DispenserLeverPull extends Verb
{
	public DispenserLeverPull()
	{
		super ("pull");
		alias ("slide");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		
		Thing lever = d.verbObject();
		Player p = d.subject();
		Location l = d.place();
		Location t = (Location) lever.getThing("target room");

		if (d.directObject() == lever)
		{
			Object[] pPush = {"You slide the lever up and down a few times, but nothing particularly interesting happens."};
			Object[] oPush = {p," works the lever on ",lever," a few times, but nothing interesting happens."};
			l.tellAll(p, pPush, oPush);

			if (!t.getBool("alert on"))
			{
				t.putDescriptor("alert", "A pair of bright red rotating emergency lights suspended from the ceiling bathe the room in a bloody glow, while an ominous air raid siren wails on and off in the distance.");
				t.tellEverybody("A pair of rotating emergency lights descend from hidden compartments in the ceiling, filling the room with a flashing red glow as the wail of a loud air raid siren begins to echo through the room.");
				t.tellEverybody("\"WARNING!\" a computerized voice announces, \"NULL DISPENSER EXCEPTION. PLEASE REMAIN CALM AND FOLLOW EMERGENCY PROCEDURES.\"");
				t.putBool("alert on", true);

				t.handleDelayedEvent(new RealEvent("shutdown",null,null),1);
			}
			return true;
		}
		else
			return false;
	}
}
