package demo;

import twisted.reality.*;

public class PaintingDescription extends DynamicProperty
{
	public Object value(Thing painting, Thing observer)
	{
		String descstring = painting.DESC();
		Thing rec = painting.getThing("reciever");
		Location rl = null;
		if (rec != null)
			rl = rec.place();
		String locString = "Nowhere";
		if (rl != null)
			locString = rl.name();
		
		descstring += " A small brass plaque is set into the bottom of the frame, engraved with the words \"Location: "+locString+"\", and a small black button labeled \"Page\".";

		return descstring;
	}
}
