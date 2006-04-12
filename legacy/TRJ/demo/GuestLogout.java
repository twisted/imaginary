package demo;

import twisted.reality.*;
import java.util.Enumeration;
public class GuestLogout extends RealEventHandler
{
	public void gotEvent(RealEvent re, Thing thisThing)
	{
		Location defaultRepop = (Location)thisThing.getThing("default repop");
		Enumeration stuff = ((Player)thisThing).things();
		while(stuff.hasMoreElements())
		{
			Thing tht = (Thing)stuff.nextElement();
			Location repop = (Location)tht.getThing("repop");
			if (repop == null)
				repop=defaultRepop;
			Object[] leavearrive={Name.Of(tht)," repopulates."};
			tht.setComponent(false);
			// just in case it was a piece of clothing
			tht.removeProp("clothing worn");
			tht.moveTo(repop,leavearrive);
		}
		thisThing.dispose();
	}
}
