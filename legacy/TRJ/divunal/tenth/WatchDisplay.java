package divunal.tenth;

import twisted.reality.*;

public class WatchDisplay extends DynamicProperty
{
	public Object value(Thing o, Thing d)
	{
		String descstring;
		String ampm;
		int time = random()%13;
		long cri = System.currentTimeMillis();
		float tir = random()%100;

		if (randomf() > 0.5)
			ampm = "AM";
		else
			ampm = "PM";

		descstring = o.getString("base description")+" The hands of the watch indicate that it is currently "+time+" o'clock "+ampm+", and a smaller set of numerical displays on the face of the watch show a \"Chrono-Referential Index\" of "+cri+" and a \"Tachyon Interference Rating\" of "+tir+"%.";

		return descstring;
	}
}
