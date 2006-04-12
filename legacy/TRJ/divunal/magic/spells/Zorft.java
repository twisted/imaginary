package divunal.magic.spells;
import divunal.magic.Spell;
import twisted.reality.*;

public class Zorft extends Spell
{
	public String spellName()
	{
		return "zorft";
	}
	
	public void spellEffect(Player caster,
							Location place,
							Thing affected)
							throws RPException
	{
		if (affected.getBool("isLit"))
		{
			if (affected.getBool("frotzed"))
			{
				affected.mood(null);
				affected.removeDescriptor("lighting");
				affected.removeProp("frotzed");
				affected.putBool("isLit",false);
				Object[] zft = {"You mutter the gutteral tones of Zorft to yourself."};
				Object[] teb = {caster," growls a few low syllables, which sound like distant thunder."};
				
				place.tellAll(caster,zft,teb);
				Object[] effect = {
					"There is an almost audible draining of light as ",
					affected,
					" ceases to glow.  The darkness fades to a less disturbing level, but ",affected,
					" is now quite useless as a light source."
				};
				place.tellAll(effect);
				place.handleEvent(new RealEvent("darkcheck",null,affected));
			}
			else
			{
				caster.hears("You attempt to dispel the non-magical lighting, but it seems as thought that would require a different skill.");
			}
		}
		else
		{
			Object[] ch = {"You attempt to remove what light there is from ",
						   affected,", but appear to fail."};
			caster.hears(ch);
		}
	}
	
	public String spellDescription()
	{
		return "cause something to give off darkness";
	}
}
