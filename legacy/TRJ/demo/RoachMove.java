package demo;

import twisted.reality.*;

public class RoachMove extends RealEventHandler
{
	public static final String[] bugsounds =
	{
		"The cockroach wiggles its antennae curiously.",
		"The cockroach skitters around frantically for a moment, and then comes to a rather sudden stop.",
		"The cockroach flutters its wings, emitting a faint clicking sound.",
		"The cockroach waves its antennae and wiggles its abdomen, apparently having found a small but tasty particle of something on the ground.",
		"The cockroach waves its antennae.",
		"The cockroach skitters around.",
		"The cockroach flutters its wings and suddenly takes to the air, flying around in erratic circles for a few seconds, emitting a rasping metallic buzz... and then plummets to the ground with a faint clinking sound."
	};

	public void gotEvent(RealEvent e, Thing thisThing)
	{
		Player p;
		Room r;
		String s;
		float chance = randomf();
		int winds = thisThing.getInt("winds");
		Location l = thisThing.place();
		Location ll = l.place();

		if (winds == 0)
		{
			Object[] flip = {thisThing," flips over onto its back, twitches its legs momentarily, and falls silent."};
			l.tellAll(flip);
			thisThing.mood("lying on its back");
			return;
		}

		winds -= 1;
		thisThing.putInt("winds", winds);
		thisThing.handleDelayedEvent(new RealEvent("roachmove",null,null),1);

		if (l == null)
			return;

		if(l instanceof Player)
		{
			p = (Player)l;
			Object[] elm = {thisThing," wriggles its way out of ",p,"'s hands."};
			Object[] plhr = {thisThing," wriggles out of your hands, and lands on the ground."};
			Object[] toTellAll = {thisThing," wriggles its way out of ",p,"'s hands, and lands on the ground."};
			ll.tellAll(p,plhr,toTellAll);
			thisThing.moveTo(ll, elm);
			return;
		}

		if (l instanceof Room || ll == null)
		{
			l.tellEverybody(random(bugsounds));
			return;
		}

		if(l.areContentsOperable())
		{
			Object[] rlin = {thisThing, " takes wing with a raspy metallic buzz and flies away from ", l,"."};
			Object[] rmout = {thisThing, " flies away from ",l,"."};
			
			ll.tellAll(rlin);
			
			if (l.isBroadcast())
			{
				thisThing.moveTo(ll, rmout);
			}
			else
			{
				Object[] rout = {thisThing, " takes wing with a raspy metallic buzz and flies away."};
				Object[] rmlin = {thisThing, " flies out of ",l,"."};
				
				l.tellAll(rout);
				thisThing.moveTo(l.place(), rmout, rmlin);
			}
		}
		else
		{
			if ((!l.isBroadcast()) || (!l.areContentsVisible()))
				{
					Object[] tta  = {"There is a faint scrambling sound from inside ",l,"."};
					ll.tellAll(tta);
				}

			thisThing.topPlace().tellEverybody(random(bugsounds));
		}
	}
}
