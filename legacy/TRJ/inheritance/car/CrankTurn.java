package inheritance.car;
import twisted.reality.*;

/**
 * This is the verb for cranking the starter crank 
 * in the ignition.
 *
 * @author Tenth
 */

public class CrankTurn extends Verb
{
	public CrankTurn()
	{
		super("turn");
		alias("crank");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Thing crank = d.verbObject();
		Location socket = crank.place();

		// We are cranking the CRANK, right?
		
		if (crank != d.directObject())
		{
			return false;
		}

		// We aren't sitting in the car, are we?

		if (p.place() == socket.place())
		{
			p.hears("You'll have to get out of the car to do that.");
			return true;
		}

		// The crank is in the socket, not something else, isn't it?
		
		if (!(crank.getString("type").equals(socket.getString("type"))))
		{
			p.hears("That wouldn't accomplish much at this point...");
			return true;
		}

		// You crank it, and...

		Object[] pCranks = {"You give the crank a few good turns."};
		Object[] oCranks = {p," gives the crank a few good turns."};
		d.place().tellAll(p, pCranks, oCranks);

		if (randomf() < 0.8f)
		{
			// One of two unimpressive things happen, or...

			Object[] wussCrank = null;
			if (randomf() > 0.5f)
			{Object[] wCA = {"The engine lets out a hearty belch and sputters for a few moments before coming to a stop once again."}; wussCrank = wCA;}
			else
			{Object[] wCB = {"The engine rattles and coughs weakly a few times, and then grinds to a halt."}; wussCrank = wCB;}
			d.place().tellAll(wussCrank);
		}
		else
		{
			// You start it... Well, as much as that piece of crap
			// can be started at this point...
			
			Object[] manlyCrank = {"The engine rattles fiercely for a few seconds, and begins to let out it's customary ungodly racket... And then, with a deafening backfire and a colorful burst of blue smoke from the tailpipe, it falls silent once more."};
			d.place().tellAll(manlyCrank);

			// Insert outside noise propogation event here, and scare
			// the beejesus out of any monster unfortunate enough to be
			// outside at the time.
		}
		return true;
	}
}