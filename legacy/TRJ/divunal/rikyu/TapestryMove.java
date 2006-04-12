package divunal.rikyu;

import twisted.reality.*;

public class TapestryMove extends Verb
{
	public TapestryMove()
	{
		super("move");
		alias("open");
		alias("close");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing obstructor = d.directObject();
		Room room = (Room)d.subject().topPlace();
		Portal door = room.getPortalByThing(obstructor);
		if(obstructor.getBool("obstructed"))
		{
			door.backtrack().setObvious(true);
			door.setObvious(true);
			room.putDescriptor("tapestry moved", " The northern tapestry has been moved to show a small doorway.");
			obstructor.putDescriptor("tapestry moved", " The northern tapestry has been moved to show a small doorway.");
			obstructor.putBool("obstructed", false);
		}
		else
		{
			door.backtrack().setObvious(true);
			door.setObvious(false);
			room.removeDescriptor("tapestry moved");
			obstructor.removeDescriptor("tapestry moved");
			obstructor.putBool("obstructed", true);
		}
		return true;
	}
}
