package divunal.common.author;

import twisted.reality.*;

public class CreateBox extends Verb
{
	public CreateBox()
	{
		super("box");
	}
	
	public boolean action(Sentence d)
		throws RPException
	{
		Location target;
		Location location;
		String indirectIn = null;
		Thing tmp=Age.theUniverse().findThing(d.indirectString("to"));
		if (tmp instanceof Location)
		{
			target=(Location) tmp;
		}
		else 
		{
			d.subject().hears("A box coalaces in front of you but it is hazy, it wobbles on an edge and appears to shrink, then it vanishes.");
			return true;
		}   
		try
		{
			indirectIn=d.indirectString("in");
		}
		catch(RPException e)
		{
			
		}
		
		
		if(indirectIn==null)
		{
			location=d.place();
		}
		else
		{
			tmp = Age.theUniverse().findThing(indirectIn);
			if (tmp instanceof Location)
			{
				location=(Location) tmp;
			}
			else
			{
				d.subject().hears("You hear a buzz, and a soft humm, then a click. You have a feeling something didn't work quite right.");
				return true;
			}      
		}
		
		if(location==null)
		{
			d.subject().respond("There's no such place as \""+d.indirectString("in"));
			return true;
		}
		
		if(target==null)
		{
			d.subject().respond("You see an obsidian box form for a moment, and waver, as it searches for a destination. It vanishes after a moment's questing.");
			return true;
		}
		
		Thing t = new Thing(location,generateColor(target) + " box","This appears to be a magical box.");
		
		t.name(generateColor(target) + " box");
		t.setSuperClass(Age.theUniverse().findThing("Class_Obsidian_Box"));
		
		t.putThing("magic box location",location);
		t.putThing("magic box target",target);
		
		return true;
	}
	
	public String generateColor(Thing t)
	{
		String[] colors = {"obsidian","ebony","oaken","jade","gold","crystal","diamond","translucent","ruby"};
		
		int i = t.name().hashCode();
		
		i = i % colors.length;
		
		return colors[i];
	}
}
