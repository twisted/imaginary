package twisted.reality.plugin;

import twisted.reality.*;

/**
 * This verb for giving things to other players.
 *
 * (At some point, we might want to work some sort of permission into
 * this process. -Tenth)
 * 
 * @author Bento */

public class Give extends Verb
{
	public Give()
	{
		super("give");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing t;
		Player prp = d.subject();
		try
		{
			t = d.directObject();
		}
		catch (NotInterestingException nie)
		{
			prp.hears("You don't have the "+d.directString()+".");
			return true;
		}
		if(t.place()==prp) 
		{
			Thing ido = d.indirectObject("to");
			if (ido instanceof Player) 
			{
				Player p = (Player)ido;
				Object[] giv={prp," gives ",t," to ",p,"."};
				t.moveTo(p,giv);
				Object[] givu={prp," gives you ",t,"."};
				p.hears(givu);
				Object[] gav={"You give ",t," to ", p,"."};
				prp.hears(gav);
			}
			else
			{
				Object[] cantgive={"You can't give ",t," to an inanimate object."};
				prp.hears(cantgive);
			}
		}
		else 
		{
			Object[] donthave={"You aren't carrying ",t,"."};
			prp.hears(donthave);
		}
		
		return true;
	}
} 
