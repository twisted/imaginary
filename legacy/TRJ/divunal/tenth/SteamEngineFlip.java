package divunal.tenth;

import twisted.reality.*;
import divunal.tenth.SteamEngineEvent;

public class SteamEngineFlip extends Verb
{
    public SteamEngineFlip()
    {
		super("flip");
		alias("toggle");
		alias("throw");
		alias("set");
    }

    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		String s = d.directString();
		Room room = (Room) d.place();
		Thing steamsource = d.directObject().getThing("steam source");
		String currentmagic = steamsource.getString("magic");

		if (d.hasIndirect("to"))
		{
			if (d.indirectString("to").equals("magic"))
			{
				if (currentmagic.equals("Magic"))
				{
					p.hears("The switch is already in that position.");
					return true;
				}
				else
				{
					currentmagic = "Magic";
				}
			}
			else if (d.indirectString("to").equals("more magic"))
			{
				if (currentmagic.equals("More Magic"))
				{
					p.hears("The switch is already in that position.");
					return true;
				}
				else
				{
					currentmagic = "More Magic";
				}
			}
		}
		else
			if(currentmagic.equals("More Magic"))
				currentmagic = "Magic";
			else
				currentmagic = "More Magic";
		Object[] flipper = {p," flips the switch to the \"",currentmagic,"\" position."};
		Object[] flippee = {"You flip the magic switch to the \"",currentmagic,"\" position."};
		
		room.tellAll(p,flippee,flipper);
		SteamEngineEvent.toggleMagicSwitch(steamsource);
		return true;
    }
    
}
