package divunal.common.author;

import twisted.reality.*;

public class PCMachineType extends Verb
{
	public PCMachineType()
	{
		super("type");
		setDefaultPrep("on");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		Thing thing = d.indirectObject("on");
		String s = d.directString();
		d.subject().hears("");
		Object[] teb = {d.subject()," types something on ",thing,"'s keyboard."};
		Object[] tu = {"You type on ",thing,"'s keyboard."};
		d.place().tellAll(d.subject(),tu,teb);
		thing.putString("player name",s);
		thing.handleEvent(new RealEvent("update",null,thing));
		return true;
	}
}
