package inheritance.car;

import twisted.reality.*;

// This is the dynamic description for the car; It makes
// the description vary depending on your location.

public class CarLook extends DynamicProperty
{
	public Object value(Thing subject, Thing observer)
	{
		String descstring;
		Location car = (Location) subject;

		if (observer.place() == car)
			descstring = car.getString("interior description");
		else
			descstring = car.DESC();
		
		return descstring;
	}
}