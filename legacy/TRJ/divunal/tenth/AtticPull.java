package divunal.tenth;

import twisted.reality.*;

public class AtticPull extends Verb
{
	public AtticPull()
	{
		super("pull");
		alias("yank");
		alias("get");
		alias("take");
	}
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Room room = (Room)d.place();
		Thing door = room.getThing("attic staircase");
		Portal way = room.getPortalByThing(door);

		if(door.getBool("obstructed"))
		{
			Object[] ringpul={"As you pull on the ring, the board it was attached to swings out, and a wooden staircase unfolds from the ceiling."};
			Object[] pulring={p," pulls on the ring, and watches as a wooden staircase unfolds from the ceiling."};
			room.tellAll(p,ringpul,pulring);
			door.putBool("obstructed",false);

			if(way != null)
				way.setObvious(true);

			room.putDescriptor("attic door state", "A jointed wooden staircase hangs down from an opening in the ceiling, leading up into darkness.");

			door.handleDelayedEvent(new RealEvent("attic door close",null,null),1);		
		}
		else
		{
			Object[] ringpul={"You pull on the ring as hard as you can, but you get the feeling that the staircase isn't going to move any further."};
			
			Object[] pulring={p," tugs ruthlessly on the ring attached to the staircase, but fails to pull it down any further."};
			room.tellAll(p,ringpul,pulring);
		}
		return true;
	}
}
