package twisted.reality;
import twisted.util.*;

/**
 * Sets up Thing properties once all objects in the map have loaded.
 */

class ThingPropSetup extends RecursiveSetup
{
	ThingPropSetup(Thing a, String b, String c)
	{
		th=a;
		thePropName=b;
		theObjName=c;
	}
	
	public void wrapper()
	{
		Thing theObj = Age.theUniverse().findThing(theObjName);
		if (theObj == null)
			Age.log("Thing property not found: "+theObjName);
		th.putThing(thePropName,theObj);
	}
	
	Thing th;
	String thePropName;
	String theObjName;
}
