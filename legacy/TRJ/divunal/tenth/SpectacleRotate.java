package divunal.tenth;

import twisted.reality.*;

public class SpectacleRotate extends Verb
{
	public static final String[] spectaclecolors =
	{
		"mauve",
		"turqoise",
		"pink",
		"violet",
		"amber",
		"black",
		"fuscha"
	};
	
    public SpectacleRotate()
    {
		super("rotate");
		alias("twist");
		alias("turn");
		alias("adjust");
    }
    
    public boolean action(Sentence d) throws RPException
    {
			Player p = d.subject();
			Thing specs = d.directObject();
			String c, name;
			Room r = (Room) d.place();

			c = random(spectaclecolors);
			Object[] fiddles = {p, " fiddes with ",Name.of(specs,p),", and the lenses shift to an odd "+ c +" coloration."};
			Object[] twist = {"You give the lenses an experimental twist, and they shift into sort of a " + c + " color."};
			r.tellAll(p,twist,fiddles);
			specs.putString("color", c);
			name = "pair of " + c + "-tinted spectacles";
			specs.putString("name", name);
			specs.putString("clothing appearance", "a "+name);
			specs.describe("A pair of brass framed spectacles with "+ c +" colored lenses, each of which is set in some sort of odd mechanism which apparently allows them to be rotated.");
			Location specsPlace=specs.place();
			// specs.place(specsPlace);
			twisted.reality.plugin.clothes.WearRemove.descript(specsPlace);
			return true;

	}
    
}
