package divunal.tenth;

import twisted.reality.*;
import divunal.tenth.LibraryPush;
import divunal.tenth.SteamEngineEvent;

public class LibraryPull extends Verb
{
    public LibraryPull()
    {
		super("pull");
    }
    
    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		String s = d.directString();
		Room room = (Room) d.place();
        Thing door = d.directObject().getThing("target door");
		Room oroom = (Room) door.place();
		Thing steamsource = d.directObject().getThing("steam source");
		int steampressure = steamsource.getInt("steam pressure");
		Object[] yptl={"You pull the lever."};
		Object[] wptl={p," pulls the lever."};
		room.tellAll(p,yptl,wptl);
		
		if(steampressure > 50)
		{
			LibraryPush.pushGreen(door, oroom);
			steampressure -= 100;
			SteamEngineEvent.updateSteamGauge(steamsource, steampressure);
		}
		else
		{
			room.tellEverybody("There is a hollow, metallic clunking noise from somewhere under the floor.");
			steampressure = 0;
		}
		
		SteamEngineEvent.updateSteamGauge(steamsource, steampressure);

		return true;
    }
    
}
