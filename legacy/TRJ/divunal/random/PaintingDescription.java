package divunal.random;

import twisted.reality.*;

public class PaintingDescription extends DynamicProperty
{
	public Object value(Thing o, Thing d)
	{
		String descstring = o.describe();
		int looks = d.getInt("painting looks");

		if (looks == 2)
			descstring = o.getString("description 1");
		else if (looks == 3)
			descstring = o.getString("description 2");
		else if (looks == 4)
		{
			looks = -5;
			hallucinate(d, o);
		}
			
		d.putInt("painting looks", (looks+1));
		return descstring;
	}

	public void hallucinate(Thing d, Thing painting)
	{
			Player p = (Player) d;
			p.hears("The colors of the painting begin to fill your vision, and the world spins around you...");

			try
			{
				Player dreamer = new Player(p.name()+"'s astral form", p.describe());
				dreamer.setSuperClass(Age.theUniverse().findThing("Class_Player"));
				dreamer.putThing("body", p);
				dreamer.putString("name", p.name());
				dreamer.addSyn(p.name());
				dreamer.place((Location)painting.getThing("painting realm"));
				dreamer.putHandler("startup", "divunal.random.PaintingWakeUp");
				dreamer.handleDelayedEvent(new RealEvent("startup",null,null),1);
				dreamer.transferControlTo(p);
				dreamer.setFocus(dreamer.place());
			}
			catch (ClassNotFoundException cnfe)
			{
				p.hears("...Or not.");
			}
	}
}
