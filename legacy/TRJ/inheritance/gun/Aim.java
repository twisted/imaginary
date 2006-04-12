package inheritance.gun;

import twisted.reality.*;

/**
 * Aims the gun so it may later be shot.
 */

public class Aim extends Verb
{
	public Aim()
	{
		super("aim");
		setDefault();
	}
	
	public boolean action(Sentence d) throws RPException
	{
		d.directObject().putThing("aimed at",d.indirectObject("at"));
		d.directObject().putLong("aimed time",System.currentTimeMillis());
		Object[] xxx = {"You aim the gun at ", d.indirectObject("at"), "."};
		d.subject().hears(xxx);
		return true;
	}
}
