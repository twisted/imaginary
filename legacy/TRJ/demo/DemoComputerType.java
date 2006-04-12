package demo;

import twisted.reality.*;

/**
 * This is a silly little verb so that people can try to break into
 * the password protected screensaver on my computer in the demo
 * center. Maybe later, when we implement a shell interface
 * proxy/terminal emulation in TR, we can let them do more.  ;-)
 *
 * @author Tenth */

public class DemoComputerType extends Verb
{
	public DemoComputerType()
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
		String stuff = d.directString();
		int len = stuff.length();
		Thing monitor = keyboard.getThing("monitor");
		String stars = keyboard.getString("entry");
		String vbs=d.verbString();
		String password = keyboard.getString("password");

		if (stars == null)
			stars = "";

		if (vbs.equals("press") || vbs.equals("push") || len == 1)
		{
			Object[] oHears = {p, " presses a key on ",
							   keyboard,
							   "."};

			if (stuff.startsWith("enter") || stuff.startsWith("return"))
			{
				Object[] pHears = {"You press the Enter key on ",
								   keyboard,
								   "."};
				
				if (stars.equals(password))
				{
					demo.Score.increase(p,"keyboard",50);
					monitor.putDescriptor("screen", "The screen is showing a freakishly large session of XEmacs, with several pieces of Java code opened across a number of different panes. Of particular note is the scratch buffer, in which someone has written \"Cash register: 1138.\"");
					try
					{
						keyboard.removeVerb("demo.DemoComputerType");
					}
					catch (ClassNotFoundException cnfe){}

					try
					{
						keyboard.addVerb("demo.DemoComputerLocked");
					}
					catch (ClassNotFoundException cnfe){}

					keyboard.handleDelayedEvent(new RealEvent("startup",null,null),1);
 				}
 				else
				{
					room.tellAll(p, pHears, oHears);
					room.tellEverybody("The computer emits a loud beep, and says \"Incorrect Password\" in a dry, emotionless voice.");
					stars = "";
					keyboard.putString("entry", stars);
					monitor.putDescriptor("screen","In the background, a screensaver is tracing out some trippy mathematical figures, and an \"Enter Password:\" window is open in the center of the screen, displaying an empty password field.");
				}
				return true;
			}
			else if (stuff.startsWith("back") || stuff.startsWith("del"))
			{
				Object[] pHears = {"You press the \"Backspace\" key on ",
								   keyboard,
								   "."};
				room.tellAll(p, pHears, oHears);
				if (stars.length() > 0)
					stars = stars.substring(0, (stars.length() - 1));
			}
			else if (stuff.length() == 1)
			{
				Object[] pHears= {"You press the \"",stuff,"\" key on ",keyboard,"."};
				room.tellAll(p, pHears, oHears);
				stars = stars.concat(stuff);
			}
			else
			{
				Object[] pHears = {"It's not very ergonomic to press the letters for entire words at once... perhaps you should just type what you want?"};
				Object[] tHears = {p, " looks thoughtfully at the keyboard."};
				room.tellAll(p, pHears, tHears);
			}
		}
		else
		{
			Object[] pHears = {"You type \"",stuff,"\" on ",keyboard,"."};
			Object[] oHears = {p, " types something on ",keyboard,"."};
			room.tellAll(p, pHears, oHears);
			stars = stars.concat(stuff);
		}

		if (stars.length() > 32)
		{
			String bnum = String.valueOf(stars.length() - 32);
			room.tellEverybody("The computer beeps "+bnum+" times in rapid succession.");
			stars = stars.substring(0,32);
		}

		String lnum = String.valueOf(stars.length());

		if (stars.length() < 1)
			monitor.putDescriptor("screen","In the background, a screensaver is tracing out some trippy mathematical figures, and an \"Enter Password:\" window is open in the center of the screen, displaying an empty password field.");
		else
		{
			Object[] screen = {"In the background, a screensaver is tracing out some trippy mathematical figures, and an \"Enter Password:\" window is open in the center of the screen, with ",lnum," asterisks in the password field."};
			monitor.putDescriptor("screen", screen);
		}

		keyboard.putString("entry", stars);

		return true;
	}
}
