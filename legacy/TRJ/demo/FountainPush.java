package demo;

import twisted.reality.*;

/**
 * This is the disturbing verb for the drinking fountain.
 *
 * @author Tenth */

public class FountainPush extends Verb
{
	public FountainPush()
	{
		super ("press");
		alias ("push");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		
		Location fount = (Location) d.verbObject();
		Player p = d.subject();
		Location l = d.place();
		String v = d.verbString();
		boolean spouting = fount.getBool("spouting water");

		if (d.directObject() != fount)
		{
			// They aren't trying to push OUR button...

			return false;
		}

		Object[] pPush = {"You ",v," the button on the fountain."};
		Object[] oPush = {p," ",v,"es the button on the fountain."};
		l.tellAll(p, pPush, oPush);

		if (spouting)
		{
			// If the water is already flowing, our work here is done.

			return true;
		}

		if (fount.things(true, true).hasMoreElements())
		{
			// If there is stuff in the fountain, eject the first one
			// you come across.

			Thing launched = (Thing) fount.things(true, true).nextElement();
			String[] sounds = 
			{
				"There is a rumbling sound from underneath",
				"There is a lound clanking sound from underneath",
				"There is a metallic rattling sound from beneath",
				"There is a deep, echoing rumble from beneath"
			};

			Object[] launch = {random(sounds), " the floor, and ",fount,"'s spigot bulges alarmingly as ",launched," pops out of it."};
			Object[] moved = {launched," pops out of ",fount,"."};

			l.tellAll(launch);
			launched.moveTo(l, moved);
		}
		else
		{
			fountainOn(fount);
		}

		return true;
	}

	public static void fountainOn(Thing f)
	{
		f.place().tellEverybody
			("Cool, refreshing water begins to flow from the fountain.");
		f.handleDelayedEvent(new RealEvent("startup",null,null),1);
		f.putDescriptor
			("water on", "A jet of cool, clear, refreshing water is rushing from the spigot.");
		f.addSyn("water");
		f.putBool("spouting water", true);
	}

	public static void fountainOff(Thing f)
	{
		Object[] allHear = {"Water ceases to flow from ",f,"."};
		f.place().tellAll(allHear);
		f.putBool("spouting water", false);
		f.removeDescriptor("water on");
		f.removeSyn("water");
	}
}
