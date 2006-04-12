package twisted.reality;
import twisted.util.*;

class PlacementSetup extends RecursiveSetup
{
	public PlacementSetup(String a, Thing b)
	{
		theplace=a;
		thething=b;
	}
	public void wrapper()
	{
		Location a = (Location) Age.theUniverse().findThing(theplace);
		Thing b = thething;
		if (a == null)
			Age.log("Location not found: "+theplace);
		b.place(a);
	}
	
	String theplace;
	Thing thething;
}
