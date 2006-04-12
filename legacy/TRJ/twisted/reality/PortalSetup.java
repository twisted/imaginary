package twisted.reality;
import twisted.util.*;

class PortalSetup extends RecursiveSetup
{
	public PortalSetup(Room a, String b, String c,String e,boolean f)
	{
		roomtwo=b;
		direction=c;
		mroom=a;
		door=e;
		isobv=f;
	}
	
	public void wrapper()
	{
		Room a = mroom;
		Room b = (Room) Age.theUniverse().findThing(roomtwo);
		if (b == null)
		{
			Age.log("Room not found: "+roomtwo);
		}
		if ( b == null ) return;
		String c = direction;
		Portal p = new Portal(a,b,c);
		p.setObvious(isobv);
		if (door != null)
		{
			Thing doort = Age.theUniverse().findThing(door);
			if (doort == null)
				Age.log("Portal thing not found: "+door);
			p.setThing(doort);
		}
	}
	String door;
	Room mroom;
	String roomtwo;
	String direction;
	boolean isobv;
}
