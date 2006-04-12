package divunal.james;

import twisted.reality.*;

public class Recall extends Verb
{
	public Recall()
	{
		super("recall");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		String name = d.hasDirect()? d.directString() : "default";
		Location room = d.place();
		Thing obj = d.withObject();
		Object[] A,B;
		Thing where = obj.getThing("warp " + name, room);
		if (where != null && where instanceof Location)
		{
			Object[] lookin = 
			{
				"You look in ",
				Name.of(obj,p),", find ",name,", and leave."
			};
			
			Object[] checksStuff = 
			{
				p," quickly checks ",Name.of(obj,p)," and disappears."
			};
			
			A=lookin;
			B=checksStuff;
			room.tellAll(p,A,B);
			p.place((Location) where);
		}
		else
		{
			Object[] cantFindIt=
			{
				"You can't seem to find the ", name ,
				" in ", Name.of(obj,p), "."
			};
			Object[] checksDontFind=
			{
				p," checks ",Name.of(obj,p),
				" but doesn't seem to find what ",
				Pronoun.of(p)," was looking for."
			};
			A=cantFindIt;
			B=checksDontFind;
			room.tellAll(p,A,B);
		}

		return true;
	}
}
