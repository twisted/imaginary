package divunal.maxwell;

import twisted.reality.*;

public class VoiceTeleport extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		Thing p = e.origin();
		
		Thing t = thisThing.getThing("teleport phrase "+e.arg());
		if(t != null)
		{
			if (!(t instanceof Room))
			{
				if ( (t.place()!=null) && (t.place() instanceof Room))
					t=t.place();
				// If this isn't the case, we shouldn't be going there
				// [ go go gadget archetype ]
				else return;
			}
			Object[] leave={Name.Of(p)," becomes blurred, then translucent, and disappears."};
			Object[] arrive={"A colorful translucent blur appears, eventually coalescing into ", p, "."};
			
			p.moveTo((Location)t,leave,arrive);
			if (p instanceof Player)
			{
				((Player)p).hears("You hear a rainbow blur and see a faint buzzing noise.");
			}
			if (thisThing.place() instanceof Room)
			{
				String displaymessage = thisThing.getString("teleport message");
				if (displaymessage!=null)
				{
					((Room)thisThing.place()).tellEverybody(displaymessage);
				}
			}
		}
	}
}
