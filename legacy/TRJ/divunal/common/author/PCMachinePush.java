package divunal.common.author;

import twisted.reality.*;

public class PCMachinePush extends Verb
{
	public PCMachinePush()
	{
		super("push");
		alias("press");
		alias("kick");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing diro = d.directObject();
		Thing tube = diro.getThing("tube");
		String s = d.directString();
		
		if (d.verbString().equals("kick"))
		{
			/* don't do anything, just do the update below */
			Object[] teb = {d.subject()," gives the machine a swift kick."};
			Object[] tu = {"You give the machine a swift kick."};
			d.place().tellAll(d.subject(),tu,teb);
			diro.handleEvent(new RealEvent("update",null,diro));
			return true;
		}

		if (s.equals("generate"))
		{
			Object[] generator = {Name.Of(d.subject())," pushes the \"GENERATE\" button on the machine."};
			d.place().tellAll(d.subject(),null,generator);
			
			String mstr = diro.getString("player name");

			if (Age.theUniverse().findThing(mstr) == null)
			{
				Player p = new Player(null,mstr,"An undescribed player");
				tube.putDescriptor("my person","There appears to be a person floating in some fluid inside the tube.");
				tube.putThing("person",p);
			}
			else
			{
				Object[] lurchtube={Name.Of(tube)," lurches sideways and then re-adjusts itself."};
				d.place().tellAll(lurchtube);
			}
		}
		else if (s.equals("release"))
		{
			Object[] relpush = {Name.Of(d.subject())," pushes the \"RELEASE\" button on the machine."};
			d.place().tellAll(d.subject(),null,relpush);
			Thing newPerson = tube.getThing("person");
			if(newPerson !=null)
			{
				Object[] entering = {newPerson," floats through the wall of the glass tube and slumps to the floor."};
				newPerson.moveTo
					(d.place(),
					 entering);
				Object[] slid = {newPerson," slides out through the wall of the glass tube."};
				d.place().tellAll(slid);
				diro.getThing("tube").putDescriptor("my person","It appears to be filled with fluid.");
			}
			else
			{
				d.place().tellEverybody("You hear a faint sloshing sound.");
			}
		}
		else if (s.equals("randomize"))
		{
			Thing str = diro.getThing("strength");
			Thing dex = diro.getThing("dexterity");
			Thing ndu = diro.getThing("endurance");
			Thing mem = diro.getThing("memory");
			Thing agl = diro.getThing("agility");
			Thing psy = diro.getThing("psyche");

			float rnd1, rnd2, rnd3, rnd4, rnd5, rnd6;
			rnd1 = divunal.Divunal.makeModifier();
		    rnd2 = divunal.Divunal.makeModifier();
			rnd3 = divunal.Divunal.makeModifier();
			rnd4 = divunal.Divunal.makeModifier();
			rnd5 = divunal.Divunal.makeModifier();
			rnd6 = divunal.Divunal.makeModifier();
			
			rnd1 = funkify (rnd1);
			rnd2 = funkify (rnd2);
			rnd3 = funkify (rnd3);
			rnd4 = funkify (rnd4);
			rnd5 = funkify (rnd5);
			rnd6 = funkify (rnd6);
			
			str.putFloat("value",rnd1);
			dex.putFloat("value",rnd2);
			ndu.putFloat("value",rnd3);
			agl.putFloat("value",rnd4);
			mem.putFloat("value",rnd5);
			psy.putFloat("value",rnd6);
			
			Object[] rndm={Name.Of(d.subject())," pushes the \"RANDOMIZE\" button on the machine."};
			d.place().tellAll(d.subject(),null,rndm);
			Object[] buzzr = {Name.Of(diro)," makes a loud buzzing noise."};
			d.place().tellAll(buzzr);
			
		}
		else
		{
			return false;
		}
		diro.handleEvent(new RealEvent("update",null,diro));
		return true;
	}
	
	float funkify(float f)
	{
		f -= f % 0.05;
		return f;
	}
}
