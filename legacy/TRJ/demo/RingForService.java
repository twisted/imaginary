package demo;

import twisted.reality.*;

public class RingForService extends Verb
{
	public RingForService()
	{
		super("ring");
		alias("press");
		alias("push");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing bell = d.directObject();
		Player p = d.subject();
		Room r = (Room) d.place();
		Thing reciever = bell.getThing("reciever");
		Location rr = reciever.place();
		Room rroom;
		
		Object[] pHears = {"You press the bell, and it emits a faint ringing sound."};
		Object[] oHears = {p, " presses the bell, and it emits a faint ringing sound."};
		r.tellAll(p, pHears, oHears);

		if (rr instanceof Room)
			rroom = (Room) rr;
		else
			if (rr.place() instanceof Room)
				rroom = (Room) rr.place();
			else
				return true;		
		
		Object[] aTell = {Name.Of(reciever), " emits a faint, echoing ring, and for a moment, a fuzzy black and white image of ",p," ringing a bell in ",r," hovers above it."};

		rroom.tellAll(aTell);
		return true;
	}
}
