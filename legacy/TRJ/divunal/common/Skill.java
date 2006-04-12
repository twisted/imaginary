package divunal.common;

import twisted.reality.*;
import divunal.Divunal;

// The Skill class extends the Verb class, and adds a bunch of methods.
// By default, new skills will have standardized learnSkill and getCurrentSkill
// methods, and default to a 0.03 daily increment. You will definitely want
// to override relevantStat (so your skill doesn't always depend on Dexterity)
// and you can also override anything else you want... but make sure you
// understand how the defaults work first.

// If you make a totally wacky new Skill, and override everything, you should
// make sure that at the very least, you have a working learnSkill method,
// because Ability-bestowing objects in Divunal may attempt to call it.

// The other methods are normally only used by the verb action code,
// but it's good practice to make sure they're around and produce output
// similar to the defaults, in case anyone else tries to use them.

public abstract class Skill extends Verb
{
	// Some magic stuff that makes the verb work and be named correctly
	public Skill (String s){super(s); skname = s;}
	String skname;

	// How much the skill rises if it has been successfully used that day.
	// Using the skill repeatedly can increase this ammount, but only to
	// about double the increment, and that takes a LOT of work.
	public float dailyIncrement() {return 0.03f;} // default value

	// The stat that the skill is based on
	public String relevantStat() {return "dexterity";} // default value

	// The name of the skill when stored (defaults to the class name)
	public String skillName() {return skname;} // default value

	// Whether characters can teach the skill to each other.
	public boolean teachable() {return false;} // default value

	public float initialValue() {return 0.1f;}

	// A method which seems complex, but really just records the
	// number of times that the player has used the skill that day.
	// 
	// Each day, if you have used the skill, the daily increment is
	// added to your skill modifer. Using the skill repeatedly will
	// increase the ammount you get, but you can't get more than
	// double the daily increment, and that takes a LOT of practice.

	public void updateSkill(Player p)
	{
		twisted.reality.Stack skillUpdates = (twisted.reality.Stack) p.getPersistable("updatedSkills");

		if (skillUpdates == null) skillUpdates = new twisted.reality.Stack();

		if (!skillName().equals(skillUpdates.peekString()))
			skillUpdates.pushString(skillName());
		
		p.putPersistable("updatedSkills", skillUpdates);
	}

	// The method called when the player has done something which has
	// allowed them to learn the skill... This is where you should put
	// any additional requirements you want it to have (stat requirements,
	// prequisite skills, etc.)

	public boolean learnSkill(Player p)
	{
		String sname = skillName();
		// If you already have a skill rating, you can't learn the
		// skill again.

		if (!(p.getFloat(sname) == 0))
		{
			p.hears("You've already learned to do that.");
			return false;
		}

		// Since you're learning it, be sure to make it not be zero anymore.
		// As you can see above, a skill of 0 is the same as never having
		// learned the skill at all.

		p.putFloat(sname, initialValue());
		return true;
	}

	// This method returns your character's current skill... If you
	// want to change the way this works, make sure that your system
	// is consistant with this one.

	public float getCurrentSkill(Player p)
	{
		String sname = skillName();
		String rstat = relevantStat();
		float skillModifier = p.getFloat(sname);
		float stat = Divunal.statGetCurrent(p, rstat);

		// The skill returned will be between -1 and +1, just like a stat.

		// The base level your skill starts at is equal to a percentage of
		// your relevant stat, on a scale of -1 to +2 (minimum worst starting
		// level to totally maxxed out). The base is recalculated each time
		// you get your current skill, in case your stats have changed.

		float skillBase = (((stat+1) / 3) * 2) - 1;

		// You get a skill modifier from practicing your skill... This starts
		// at 0, and can get up to 0.5, and is added to your base to get your
		// current skill.

		float skillValue = skillBase + skillModifier;

		// So... After all that, we end up with a nice, simple
		// number between -1 and +1.  :-)

		return skillValue;
	}
}
