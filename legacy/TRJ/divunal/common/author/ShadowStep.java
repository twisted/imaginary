package divunal.common.author;
import twisted.reality.*;

/* Named in deference to Roger Zelazny's Amber books. This can be used
to travel outwards into the location that a room (or set of rooms) is
grouped in, or to quickly move into a room being stored in your
current location. */

public class ShadowStep extends Verb
{
    public ShadowStep()
    {
		super("shadowstep");
    }

    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		Location here = d.place();
		Location there = null;

		if (d.hasDirect())
		{
			if(d.directObject() instanceof Location)
				there = (Location) d.directObject();
		}
		else if (d.hasIndirect("in"))
		{
			if (d.indirectObject("in") instanceof Location)
				there = (Location) d.indirectObject("in");
		}
		else if (d.hasIndirect("to"))
		{
			if (d.indirectObject("to") instanceof Location)
				there = (Location) d.indirectObject("to");
		}
		else
		{
			there = here.place();
		}

		if (there == null)
		{
			String[] direction = {"slightly to one side","a bit to the left","a bit to the right", "around"};
			String[] suffix = {" and stares off into space.", " tracing an invisible wall.", " and stops, raising one hand as if testing an invisible wall."};
			String dir = random(direction);
			String suf = random(suffix);

			Object[] pLeaves={"You press tentatively outwards, but touch nothing but the void."};
			Object[] oLeaves={p, " turns ",dir,suf};
			here.tellAll(p,pLeaves,oLeaves);
		}
		else
		{
			Object[] stepOut = {p," steps sideways into nothingness"};
			Object[] stepIn = {p," steps sideways out of nothing"};
			Object[] pLeaves={"You take a step sideways, out into ",there,"."};
			Object[] oLeaves={p, " steps a step to one side, disappearing behind the edge of a nonexistant corner."};
			Object[] aArrives={p, " steps out from behind the edge of a nonexistant corner."};
			here.tellAll(p,pLeaves,oLeaves);
			there.tellAll(aArrives);
		
			p.moveTo(there, stepOut, stepIn);
		}
		return true;
    }
}
