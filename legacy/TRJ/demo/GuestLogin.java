package demo;

import twisted.reality.*;

/**
 * This eventhandler should be called upon a guest logging in.
 */

public class GuestLogin extends RealEventHandler
{
	int guestPlayerPosition=0;
	public void gotEvent (RealEvent re, Thing thisThing)
	{
		Player guestroot=(Player) thisThing;
		int startpos = Math.abs(random()) % guestColors.length;
		guestPlayerPosition = startpos;
		boolean found = false;
		String s;
		String color;
		do
		{
			color = guestColors[guestPlayerPosition];
			s = color+" Guest";
			if (Age.theUniverse().findThing(s)==null)
			{
				found = true;
				break;
			}
			guestPlayerPosition = (guestPlayerPosition + 1) % guestColors.length;
		} while (guestPlayerPosition != startpos);
		
		if(!found)
		{
			guestroot.alert("Sorry!  There are too many guests logged in right now.  Please try again later.");
			Age.theUniverse().disconnect(guestroot);
			return;
		}
		
		Player plr = new Player(s,"");
		plr.putString("adjective",color);
		plr.addSyn("guest");
		plr.addSyn(color);
		plr.setSuperClass(guestroot.getThing("playerclass"));
		guestroot.putInt("guest number",guestPlayerPosition);
		plr.transferControlTo(guestroot);
		plr.place((Location)guestroot.getThing("guest start"));
		plr.hears("You are: "+plr.name());
		Score.init(plr,0,1024);
		//guestroot.swapControlWith(plr);
	}
	String[] guestColors=
	{
		"Enterprise-Wide",
		"Networked",
		"Dynamic",
		"Multitasking",
		"Robust",
		"Multiuser",
		"Internet-Enabled",
		"Cross-platform",
		"Open-Source",
		"Scratch-and-Sniff",
		"Java",
		"Scalable",
		"Fault-Tolerant",
		"Mission-Critical",
		"Intuitive"
	};
}
