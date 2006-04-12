package inheritance.clock;

import twisted.reality.*;
import java.text.*;
import java.util.Date;

public class ClockLook extends DynamicProperty
{
	public Object value(Thing o, Thing d)
	{
		String descstring;
		long initTime = o.getLong("init time");
		long gameStartTime = o.getLong("game start time");
		long currentTime = System.currentTimeMillis();
		String afterTime = o.getString("after time string");
		
		// Current Game Time = Actual System Time minus the Last 
		// Time the Game was Initialized + the time it was in the
		// game when the game started.  ;-)

		long currentGameTime = (currentTime - initTime) + gameStartTime;
		SimpleDateFormat inheritanceFormat = new SimpleDateFormat ("h:mm a");
		Date currentDate = new Date(currentGameTime);
		String dateString = inheritanceFormat.format(currentDate);

		// This causes the player to see the description, the current
		// "in character" time, and a little extra string afterwards
		// to keep the description readable. Periods are good.  ;-)

		return o.DESC()+dateString+afterTime;
	}
}
