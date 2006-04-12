package divunal.magic.spells;
import twisted.reality.*;
import divunal.magic.Spell;

public class Frotz extends Spell
{
	public String spellName()
	{
		return "frotz";
	}
	
	public void spellEffect(Player caster,
							Location place,
							Thing affected)
							throws RPException
	{
		if(affected.getBool("isLit"))
		{
			Object[] beginsglow={Name.Of(affected)," begins glowing... wait, it already was."};
			caster.hears(beginsglow);
		}
		else
		{
			affected.putBool("isLit",true);
			affected.putBool("frotzed",true);
			
			Object[] perspectivized = {"A pure white glow eminates from ",
									   affected,", bathing ",
									   Pronoun.obj(affected),
									   " in light."};
			
			affected.putDescriptor ("lighting", perspectivized);
			
			affected.mood("providing light");

			Object[] incant = {"You proudly incant the mystic syllables of ancient Frotz!"};
			Object[] mutter = {caster," mutters something unintelligible, concentrating intently."};
			place.tellAll(caster,incant,mutter);
			Object[] effect = {"There is an almost blinding flash of light as ",affected," begins to glow! It slowly fades to a less painful level, but ",affected," is now quite usable as a light source."};
			place.tellAll(effect);
			place.handleEvent(new RealEvent("darkcheck",null,affected));
		}
	}
	public String spellDescription()
	{
		return "cause something to give off light";
	}
}
