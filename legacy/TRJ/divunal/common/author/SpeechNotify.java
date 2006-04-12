package divunal.common.author;

import twisted.reality.*;

// This causes a response processor to open when someone talks 
// in the same room as your character... It was meant as a vaguely
// Instant Messenger-like notification that you should pay attention
// to your character.

public class SpeechNotify extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		Thing p = e.origin();
		String speech = (String) e.arg();
		Player notifiedPlayer = (Player) thisThing;

		if (p == notifiedPlayer)
		{
			notifiedPlayer.removeHandler("say");
			notifiedPlayer.hears("You say \""+speech+"\".");
			notifiedPlayer.hears("*** No longer Listening ***");
			return;
		}
		if (p instanceof Player)
		{
			notifiedPlayer.requestResponse(null, p+" says:", speech);
		}
	}
}
