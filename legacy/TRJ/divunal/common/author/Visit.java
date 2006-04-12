package divunal.common.author;
import twisted.reality.*;

/**
 * This allows a God to teleport to the Room closest to a desired Thing,
 * With flashy efffects.<p>
 *
 * Usage: <code>&gt; visit <b>&lt;thing to visit&gt;</b></code>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author David Sturgis
 */

public class Visit extends Verb
{
	public Visit()
	{
		super("visit");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Room r = (Room) d.place();

		if (!d.subject().isGod()) 
		{
			Object[] pDumb = {"You reach out with your mind... and don't find much."};
			Object[] oDumb = {p," furrows ", Name.of("brow",p)," in concentration... and then just looks confused."};

			r.tellAll(p, pDumb, oDumb);
			return false;
		}

		Thing t = Age.theUniverse().findThing(d.directString());

		if (t == null)
		{
			p.hears("You can't find anything by that name...");
			return true;
		}

		Room tr;
		Location tl = t.place();
		
		if (tl==null)
		{
			p.hears("You can't visit something that's nowhere...");
			return true;
		}

		if (t instanceof Room)
			tr = (Room) t;
		else if (tl instanceof Room)
			tr = (Room) tl;
		else if (tl.place() instanceof Room)
			tr = (Room) tl.place();
		else
		{
			p.hears("This probably isn't a good time to visit.");
			return true;
		}

		Object[] pHears = {"You close your eyes in concentration, searching for ",t,"..."};
		Object[] oHears = {p, " closes ", Name.of("eyes",p)," in concentration."};
		r.tellAll(p, pHears, oHears);

		String vcolor = p.getString("visit color");
		if (vcolor == null)
			vcolor = "blue";
		Object[] targetHears = {"Streaks of ",vcolor," light appear in the air, scattered randomly at first... but then beginning to trace a distinct shape in the air beside you."};
		Object[] othersHear ={"Streaks of ",vcolor," light begin to form in the air near ",t,"."};
		tr.tellAll(t, targetHears, othersHear);
		
		p.delay(5);

		Object[] leaveHears = {p, " takes a step forward and vanishes through an invisible doorway."};
		Object[] pArrives = {"The ",vcolor," streaks converge, and there is a brief flash of light as ",p," steps out the hole they leave in the air."};
		Object[] moveArrive = {p," steps through a ",vcolor," flash of light."};
		Object[] moveLeave = {p," steps through an invisible doorway."};

		if (!(t instanceof Room))
		{
			r.tellAll(p, null, leaveHears);
			tr.tellAll(pArrives);
		}
		p.moveTo(tr, moveLeave, moveArrive);

		return true;
	}
}
