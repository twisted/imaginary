package divunal.rikyu;

import twisted.reality.*;
import divunal.magic.Spell;

public class Posess extends Spell
{
    public String spellName(){ return "posess";}

    public void spellEffect(Player caster, Location place, Thing affected) throws RPException
    {
	Player newPlayer = null;
	try
	{
		newPlayer = (Player)affected;
	}
	catch(ClassCastException e){throw new FailedMagic(this);}

	newPlayer.transferControlTo(caster);
	newPlayer.focusRefreshMyObservers();
     }

     public String spellDescription()
     {
	return "steal someone's body";
     }
}
