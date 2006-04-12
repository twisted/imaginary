package twisted.reality;
import twisted.util.*;

class SuperSetup extends RecursiveSetup
{
	public SuperSetup(String a, Thing b)
	{
		theprop=a;
		thething=b;
	}
	public void wrapper()
	{
		Thing t = Age.theUniverse().findThing(theprop);
		if (t == null)
		{
			Age.log("Superclass not found: "+theprop);
		}
		thething.setSuperClass(t);
	}
	
	String theprop;
	Thing thething;
}
