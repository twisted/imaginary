package inheritance.car;
import twisted.reality.*;

/**
 * This is the verb for putting the starter crank into the ignition
 * It makes sure you're outside the car, and using the right kind of
 * crank.
 *
 * @author Tenth
 */

public class SocketPut extends Verb
{
	public SocketPut()
	{
		super("put");
		alias("insert");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Thing clip = null;
		Thing crank = d.directObject();
		Location socket = (Location)d.verbObject();
		
		if (d.hasIndirect("in"))
		{
			if (d.indirectObject("in") == socket)
			{
				if (crank.place() != p)
				{
					p.hears("You don't have one of those.");
					return true;
				}
				if (p.place() == socket.place())
				{
					p.hears("You'll have to get out of the car to do that.");
					return true;
				}
				if (socket.thingCount() > 0)
				{
					p.hears("There's already something in the socket.");
					return true;
				}
				if (socket.getString("type").equals(crank.getString("type")))
				{
					Object[] pPuts = {"You fit the starter crank into the socket."};
					Object[] oPuts = {p," puts the starter crank into the socket."};
					d.place().tellAll(p, pPuts, oPuts);
					crank.place(socket);
					return true;
				}
			}	  
		}
		return false;
	}
}
