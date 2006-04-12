package divunal.tenth;

import twisted.reality.*;

public class LibraryCloseHandler extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		if(!thisThing.getBool("obstructed"))
		{
			thisThing.putBool("obstructed",true);
			Room r =  ((Room)thisThing.place());
			Portal way = r.getPortalByThing(thisThing);
			
			way.setObvious(false);
			way.backtrack().setObvious(false);
			r.tellEverybody("There is a hissing sound as the bookshelves slide back into their original positions, obscuring the doorway to the north.");
			Room or = way.sRoom();
			or.tellEverybody("The door swings shut with a loud slam.");
			or.putDescriptor("bookshelf door","The southern door is closed.");
			r.removeDescriptor("bookshelf door open");
		}
	}
}
