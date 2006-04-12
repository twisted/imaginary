package divunal.james;

import twisted.reality.*;

public class Mark extends Verb
{
	public Mark()
	{
		super("mark");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		String name = d.hasDirect()? d.directString() : "default";
		Location room = d.place();
		Thing obj = d.withObject();
		
		obj.putThing("warp " + name, room);
		Object[] toPlayer =
		{
			"You mark down the location of this room in ",
			Name.of(obj,p), " next to the word ",name,"."
		};
		Object[] toOther =
		{
			p," makes a mark in ",Name.of(obj,p),"."
		};
		room.tellAll(p,toPlayer,toOther);
		return true;
	}
}
