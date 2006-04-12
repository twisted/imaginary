package divunal.agentmoore;

import twisted.reality.*;

public class Shoot extends Verb
{
    public Shoot()
	{
		super ("shoot");
    }

    public boolean action(Sentence d) throws RPException
    {
		Thing t = d.directObject();
		Thing l = Age.theUniverse().findThing("Hell");
		Thing wo = d.withObject();
		if (t instanceof Player) 
		{
			if (!(t == d.subject())) 
			{
				Player p = (Player)t;
				Object[] ashotb = {d.subject()," shoots ",p," who then disappears!"};
				Object[] yshotb = {"You shoot " + p.name() + " in the head with ",wo};
				Object[] ashotu = {d.subject()," shoots you, sending you reeling!"};
				
				Object[] dsp = {p, "disappears."};
				d.place().tellAll(d.subject(),p,yshotb,ashotu,ashotb);
				p.moveTo((Location)l,dsp);
			} else 
			{
				d.subject().hears("Are you a dumbass or something?");
			}
		} else 
	    {
			d.subject().hears("Shooting inanimate objects will accomplish nothing.");
		}
		return true;
    }
}
