package divunal.common;

import twisted.reality.*;

public class DarkCheck extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing thisThing)
	{
		if(thisThing.getBool("isLit",thisThing))
		{
			if (thisThing.getString("description") == null) return;
			thisThing.removeProp("description");
			thisThing.removeProp("name");
			/*thisThing.removeProp("inhibit_exits");
			  thisThing.removeProp("inhibit_items");*/
			if (thisThing instanceof Location)
			{
				Location l = (Location) thisThing;
				l.setContentsVisible(true);
				l.setContentsOperable(true);
				if (l instanceof Room)
				{
					Room r = (Room) l;
					r.setPortalsVisible(true);
				}
			}
		}
		else
		{
			if (thisThing.getString("description") != null) return;
			thisThing.putString("description",thisThing.getString("darkDescription"));
			/*thisThing.putBool("inhibit_exits",true);*/
			
			thisThing.putString("name","A Dark Place");
			/*thisThing.putBool("inhibit_items",true);*/
			if (thisThing instanceof Location)
			{
				Location l = (Location) thisThing;
				l.setContentsVisible(false);
				l.setContentsOperable(false);
				if (l instanceof Room)
				{
					Room r = (Room) l;
					r.setPortalsVisible(false);
				}
			}
		}
		/* Age.log("evt"); */
		thisThing.focusRefreshMyObservers();
	}
}
