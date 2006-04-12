package divunal.random;

import twisted.reality.*;

public class PaintingWakeUp extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		Player p;
		Player body;
		Location r, br;

		p = (Player)thisThing;
		r = (Location)p.place();
		body = (Player)p.getThing("body");
		br = (Location)body.place();
		Object[] phears = {"You begin to feel lightheaded, and the colors of this strange place begin to swirl before your eyes..."};
		Object[] ophears = {p, " looks distant for a moment... And then fades into nothingness."};
		Object[] obhears = {body, " starts suddenly, and blinks a few times."};

		r.tellAll(p, phears, ophears);
		br.tellAll(obhears);

		body.transferControlTo(p);
		p.dispose();
	}
}
