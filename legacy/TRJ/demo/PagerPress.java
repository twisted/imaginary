package demo;

import twisted.reality.*;

public class PagerPress extends Verb
{
	public PagerPress()
	{
		super("press");
		alias("push");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing button = d.directObject();
		Player p = d.subject();
		Room r = (Room) d.place();
		Player rp = (Player) button.getThing("reciever");

		if (rp == null || rp.place() == null)
		{
			Object[] pNoDice = {"You press the button on ",button," and there is a hollow, empty click."};
			Object[] oNoDice = {p, " presses the button on ",button," and there is a disappointingly hollow click."};
			r.tellAll(p, pNoDice, oNoDice);
			return true;
		}

		Location rr = rp.topPlace(); // The "outermost" place
		// the player is in, making sure that nearby people will also see this.

		
		Object[] pHears = {"You press the button on ",button," and there is a feeble buzzing sound."};
		Object[] oHears = {p, " presses the button on ",button," and there is a faint buzzing sound."};
		r.tellAll(p, pHears, oHears);

		
		Object[] pTell = {"There is a jarringly loud buzzing sound, and for a moment, a fuzzy black and white image of ",p," pushing the button on your painting in ",r," hovers before your eyes."};
		rp.hears(pTell);

		if (rp.getBool("pageable"))
			rp.requestResponse(null, "You've been Paged!", "There is a jarringly loud buzzing sound, and for a moment, a fuzzy black and white image of "+p.name()+" pushing the button on your painting in "+r.name()+" hovers before your eyes.");

		return true;
	}
}
