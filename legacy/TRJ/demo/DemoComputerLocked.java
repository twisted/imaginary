package demo;

import twisted.reality.*;

/**
 * This is a silly little verb so that people can try to break into
 * the password protected screensaver on my computer in the demo
 * center. Maybe later, when we implement a shell interface
 * proxy/terminal emulation in TR, we can let them do more.  ;-)
 *
 * @author Tenth */

public class DemoComputerLocked extends Verb
{
	public DemoComputerLocked()
	{
		super("type");
		alias("press");
		alias("push");
		setDefaultPrep("on");
	}

	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Location room = d.place();
		Thing keyboard = d.verbObject();
		Thing monitor = keyboard.getThing("monitor");
		String v = d.verbString();

		if (d.hasIndirect("on"))
			if (d.indirectObject("on") != keyboard)
			{
				return false;
			}

		String[] angryXEmacs = 
		{
			"Something to the effect of a buffer context not being opened.",
			"Something to the effect of a recursive edit not being in progress.",
			"It seems to be complaining about Control Alt Meta underscore not being defined.",
			"It looks sort of like the LISP equivalent of explosive diarrhea.",
			"It is apparently requesting you to recursively close a buffer context. Or something.",
			"If you didn't know better, you'd say it was some of the code from a EmacsLisp version of Advent.",
			"Something about EmacsLisp \"Tiring of your shallow, mortal desire to save the buffer in progress.\"",
			"Some error about XEmacs running out of Virtual Parenthesis...",
			"An error about an \"Unknown Directive Pragma\"."
		};

		Object[] pHears = {"The computer beeps repeatedly, and a message appears at the bottom of the screen... ",random(angryXEmacs)};

		if (v.equals("press") || v.equals("push"))
		{	
			if (d.directString().length() == 1)
			{
				Object[] oPresses = {p, " presses a key on ",keyboard,"."};
				room.tellAll(p, pHears, oPresses);
			}
			else
			{
				Object[] peHears = {"It's not very ergonomic to press the letters for entire words at once... perhaps you should just type what you want?"};
				Object[] oeHears = {p, " looks thoughtfully at the keyboard."};
				room.tellAll(p, peHears, oeHears);
			}
		}
		else
		{
			Object[] oTypes = {p, " types something on ",keyboard,"."};
			room.tellAll(p, pHears, oTypes);
		}

		return true;
	}
}
