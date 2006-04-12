package divunal.tenth;

import twisted.reality.*;
import divunal.tenth.LibraryPush;
import divunal.tenth.SteamEngineEvent;

public class SteamEnginePull extends Verb
{
    public SteamEnginePull()
    {
		super("pull");
    }

    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		String s = d.directString();
		Room room = (Room) d.place();
		Thing steamsource = d.directObject().getThing("steam source");
		int steampressure = steamsource.getInt("steam pressure");
		Object[] pullLever = {"You pull the lever."};
		Object[] pullsLever = {p," pulls the lever."};
		room.tellAll(p,pullLever,pullsLever);
		
		if(steampressure > 50)
		{
			steampressure = 0;
			SteamEngineEvent.updateSteamGauge(steamsource,steampressure);
			room.tellEverybody("There is a piercing whistle as gouts of steam shoot out of the valves and fittings all over the steam engine... And then it falls ominously silent.");
		}
		else
		{
			room.tellEverybody("There is a hollow, metallic clunking noise from somewhere inside the steam engine.");
		}

		return true;
    }
    
}
