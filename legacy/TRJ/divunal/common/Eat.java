package divunal.common;

import twisted.reality.*;

public class Eat extends Verb
{
    public Eat()
    {
		super("eat");
    }
    
    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		Thing eaten = d.directObject();
		Room room = (Room) d.place();

		if (eaten.place() != p)
		{
			p.hears("You'll need to get it first.");
			return true;
		}

		Object[] oEats = {p, " eats ", eaten, "."};
		Object[] pEats = {};

		String beginning = eaten.getString("eat text 1");
		String end = eaten.getString("eat text 2");

		if (beginning != null)
		{
			if (end != null)
			{
				Object[] pE ={beginning,eaten,end}; pEats = pE;
			}
			else
			{
				Object[] pE = {beginning,eaten}; pEats = pE;
			}
		}
		else
		{
			{Object[] pE = {"You eat ",eaten,"."}; pEats = pE;}
		}

		room.tellAll(p,pEats,oEats);
		eaten.dispose();

		return true;
	}
}
