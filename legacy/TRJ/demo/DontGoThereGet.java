package demo;

import twisted.reality.*;

public class DontGoThereGet extends Verb
{
	public DontGoThereGet()
	{
		super("get");
		alias("take");
	}
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Room room = (Room)d.place();
		Thing theCrap = d.directObject();
		
		Object[] pHears = {"You really don't want to pick that up. You feel you would be somehow... tainted... by it... It's the stench, if there is such a thing... You don't want it."};

		Object[] oHears = {p, " reaches for ", theCrap, " but recoils in loathing before ",Pronoun.of(p)," can even touch it."};
		Score.increase(p,"crap",-2);
		room.tellAll(p, pHears, oHears);
		
		return true;
	}
}
