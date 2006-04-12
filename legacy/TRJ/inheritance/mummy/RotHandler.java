package inheritance.mummy;

import twisted.reality.*;

public class RotHandler extends RealEventHandler
{
	public void gotEvent(RealEvent re, Thing thisThing)
	{
		Player p = (Player) thisThing;
		int rotting_turns = p.getInt("rotting turns");
		switch(rotting_turns)
		{
		case 0:
			p.hears("Your hand itches a little bit.");
			break;
		case 1:
			p.hears("Your hand itches, and feels a little funny.");
			break;
		case 2:
			p.hears("Your hand feels tingly and numb.");
			break;
		case 3:
			p.hears("Your hand is numb, and you feel a slight pain in your lower arm.");
			break;
		case 4:
			p.hears("Your hand and arm are totally numb, and you're beginning to feel ill.");
			break;
		case 5:
			p.hears("Half of your body is itching and burning like crazy.  You feel very ill, and the scent of death and rot lingers.");
			break;
		case 6:
			p.handleEvent
				(new RealEvent
					("game over",
					 "Your intreped experiment in archeology having failed, you find yourself now content to wander the halls of this bizarre mansion for the rest of eternity, occasionally moaning, occasionally feasting upon the flesh of the unwary who wander within its depraved walls.  After a while you realize that this is unusual, but the irony of your torment is now beyond your cursed cerebellum's grasp.",p));
			break;
		}
		if (rotting_turns < 6)
		{
			rotting_turns++;
			p.putInt("rotting turns",rotting_turns);
			p.handleDelayedEvent(new RealEvent("startup",null,null),1);
		}
	}
}
