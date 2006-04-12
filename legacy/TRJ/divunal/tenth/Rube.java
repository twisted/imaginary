package divunal.tenth;

import twisted.reality.*;
import divunal.Divunal;

public class Rube extends Verb
{
    public Rube()
    {
		super("rube");
    }
    
    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		Thing target =  d.directObject();
		Location l = (Location) p.getThing("teleport destination");
		Location here = d.place();
		Player t;

		if (target instanceof Player)
			t = (Player) d.directObject();
		else
		{
			p.hears("No way, dumbass.");
			return true;
		}
		Object[] ka={p," slaps a conviently placed \"DO NOT PRESS\" button, and a wooden mallet swings out from the ceiling, striking you squarely in the forehead and sending you tumbling over backwards down a polished metal slide which has opened beneath you..."};
		Object[] boom={p," slaps a conviently placed \"DO NOT PRESS\" button, and a wooden mallet swings out from the ceiling and strikes ",t," squarely in the forehead, and sending ",Pronoun.obj(t)," tumbling over backwards down a polished metal shaft which has suddenly opened in the floor and which promptly folds itself back up as though nothing unusual had happened."};
		Object[] chun={"You push The Button, and ",t," gets it."};
		here.tellAll(p,t,   chun,ka,boom   );
		
		Object[] floorfall = {t," falls through the floor "};
		Object[] ceilfall = {t," falls out of the ceiling."};
		t.moveTo(l, floorfall, ceilfall);
		
		Object[] tofaller={"You slide out of the ceiling of ",l," and fall to a painful landing on the floor."};
		Object[] toother={t," tumbles out of a hole in the ceiling and lands in a tangled heap on the ground."};
		l.tellAll(t,tofaller,toother);


		int delaytime = (int) (5 - (Divunal.endurance(t)*2));
		if (delaytime > 0)
		{
			t.hears("(You are stunned for "+delaytime+" seconds by the impact.)");
			t.delay(delaytime);
		}

		Divunal.minorStun(t, 0.5f);
		
		return true;
    }
    
}
