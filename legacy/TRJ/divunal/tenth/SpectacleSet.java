package divunal.tenth;

import twisted.reality.*;

public class SpectacleSet extends Verb
{
	public static final String[] spectacleprefixes =
	{
		" adjusts a mechanism on ",
		" rotates the lens of ",
		" switches something on "
	};
	
    public SpectacleSet()
    {
		super("set");
    }
    
    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		Thing spec = (Thing) d.directObject();
		String c = d.indirectString("to");
		String s;
		String name;
		Room r = (Room) d.place();
		
		if (p.isGod())
		{
			s = random(spectacleprefixes);
			Object[] adjustage={p, s , Name.of(spec,p), ", and the lenses shift to a transparent " , c , " color."};
			Object[] yadj={"You adjust your spectacles, setting them to " , c , "."};
			r.tellAll(p,yadj,adjustage);
			spec.putString("color", c);
			name = "pair of " + c + "-tinted spectacles";
		    spec.putString("name", name);
			spec.putString("clothing appearance", "a "+name);
			spec.describe("A pair of brass framed spectacles with "+ c +" colored lenses, each of which is set in some sort of odd mechanism which apparently allows them to be rotated.");
			Location specPlace=spec.place();
			// spec.place(specPlace);
			twisted.reality.plugin.clothes.WearRemove.descript(specPlace);
		}
		else
		{
			p.hears("You're not quite sure how to do that.");
			r.tellEverybodyBut(p, p.name()+" fiddles with the spectacles for a few seconds, and looks thoroughly confused.");
		}
		
		try
		{
			if (c.equals("blue"))
			{
				spec.addVerb("divunal.rikyu.XRayVision");
			}
			else
			{
				spec.removeVerb("divunal.rikyu.XRayVision");
			}
		}
		catch (ClassNotFoundException ce)
		{
		}

		return true;
	}
}
