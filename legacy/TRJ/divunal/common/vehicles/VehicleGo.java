package divunal.common.vehicles;

import twisted.reality.*;

/**
 * This is a replacement for the Go verb to be used in 
 * Vehicle-like things. Vehicle-like things being any 
 * container/location the player can be inside, and that
 * should move when the player wants to.
 * 
 * Usage: <code>&gt; go <b>&lt;direction&gt;</b></code>
 *
 * @version 1.0.0, 02 Oct 1999
 * @author Tenth
 */

public class VehicleGo extends Verb
{
	public VehicleGo()
	{
		super("go");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing vehicle = d.verbObject();

		if (d.subject().place() == d.verbObject())
		{
			Portal x = ((Room) vehicle.place()).getPortal(d.directString());
			Player p = d.subject();

			if(x != null)
			{
				x.propels(vehicle);
				p.setFocus(vehicle.place());
			}
			else
			{
				d.subject().hears("You can't go that way.");
			}

			return true;

		}

		return false;
	}
}
