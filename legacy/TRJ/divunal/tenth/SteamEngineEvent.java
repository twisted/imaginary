package divunal.tenth;

import twisted.reality.*;

public class SteamEngineEvent extends RealEventHandler
{	
	public static void updateSteamGauge(Thing engine, int steam)
	{
			engine.putInt("steam pressure", steam);
			engine.putDescriptor("steam descriptor", " A circular, glass covered gauge protrudes from the front of the engine, its needle hovering near the "+ steam +" PSI mark.");
	}

	public static void toggleMagicSwitch(Thing engine)
	{
		String currentmagic = engine.getString("magic");
		Room r = (Room)engine.place();
		Thing enginepump = engine.getThing("pump source");
		Room pr = (Room)enginepump.place();
		Portal way = pr.getPortalByThing(enginepump);

		if (currentmagic.equals("Magic"))
		{
			currentmagic = "More Magic";
			r.tellEverybody("There is a faint clattering noise from inside the steam engine, followed by the faint hiss of air moving through its valves.");
			pr.tellEverybody("The pump moves slightly against its constraints, and begins to produce a rhythmic humming sound.");
			enginepump.putDescriptor("pump action", " It is producing a rhythmic humming sound, and causing the water in the well below it to churn violently.");
			pr.putDescriptor("pump sound"," A rhythmic, almost mechanical humming sound echoes throughout the room.");
			enginepump.putBool("obstructed", true);
			if(way != null)
			{
				way.setObvious(false);
				Portal yaw = way.backtrack();
				yaw.setObvious(false);
			}
		}
		else
		{
			currentmagic = "Magic";
			updateSteamGauge(engine, 0);
			r.tellEverybody("The engine lets out a painfully loud, shrieking whistle as steam erupts from every valve and fitting... And then falls ominously silent.");
			pr.tellEverybody("The pump stutters momentarily, and then falls silent, as the water in the well begins to lower.");
			pr.removeDescriptor("pump sound");
			enginepump.putDescriptor("pump action", " The water level in the well is extremely low, having leveled at a point where the well shaft appears to widen into a larger chamber.");
			enginepump.putBool("obstructed", false);
			if(way != null)
			{
			    way.setObvious(true);
				Portal yaw = way.backtrack();
				yaw.setObvious(true);
			}
		}
		engine.putString("magic", currentmagic);
		engine.putDescriptor("magic descriptor", " There is a rather ominous looking throw-switch labeled \"Magic\" and \"More Magic\" attached to the base of the engine, currently set to the \""+ currentmagic +"\" position.");
	}

	public void gotEvent(RealEvent e, Thing thisThing)
	{
		Room r = (Room)thisThing.place();
		String currentmagic = thisThing.getString("magic");
		int currentsteam = thisThing.getInt("steam pressure");
		
		if (currentmagic.equals("More Magic"))
		{
			currentsteam += 50;
			if (currentsteam > 600)
			{
				r.tellEverybody("There is a loud hissing sound as steam spurts out of the valves on top of the engine.");
				currentsteam = 400;
			}
			updateSteamGauge(thisThing, currentsteam);
		}

		thisThing.handleDelayedEvent(new RealEvent("SteamEngineEvent",null,null),4);
	}
}

// Below that, there is a large brass lever with a red handle, from
// which a \"DANGER: RELEASE VALVE\" sign is han
