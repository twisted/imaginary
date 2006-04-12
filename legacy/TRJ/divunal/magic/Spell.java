package divunal.magic;

import twisted.reality.*;

public abstract class Spell extends Verb
{
	/**
	 * This works just like a Verb does.  You must declare your name
	 * in your constructor.
	 */
	
	public Spell()
	{
		/* uhhhh... do *not* do this, it's bad... */
		super(null);
		alias (spellName());
	}
	
	public abstract String spellName();
	
	public class FailedMagic extends RPException
	{
		Spell spel;
		public FailedMagic (Spell sp)
		{
			spel=sp;
		}
		public String toString()
		{
			return spel.spellError();
		}
	}

	/**
	 * This method is for spells which affect an object.  Note: if you
	 * don't override this method, the default behavior is for your
	 * spell to have an error.
	 */
	
	public void spellEffect(Player caster,
							Location place,
							Thing affected) throws RPException
	{
		throw new FailedMagic(this);
	}
	
	/**
	 * This method is for spells which do not affect an object.  Note:
	 * if you don't override this methods, the default behavior is for
	 * your spell to have an error.
	 */
	
	public void spellEffect(Player caster,
							Location place) throws RPException
	{
		throw new FailedMagic(this);
	}
	
	public final boolean action (Sentence d) throws RPException
	{
		Player sub=d.subject();
		String learnedkey = "learned "+spellName();
		int learned = sub.getInt(learnedkey);
		int alearned = sub.getInt("spells learned");
		if (learned > 0)
		{
			/* If you're trying to cast it on something, cast it on that */
			if (d.hasDirect())
			{
				spellEffect(sub,d.place(),d.directObject());
			}
			/* Otherwise, just cast it */
			else
			{
				spellEffect(sub,d.place());
			}
			learned--;
			alearned--;
			if (learned==0) learned--;
			sub.putInt(learnedkey,learned);
			sub.putInt("spells learned",alearned);
		}
		else if (learned == 0)
		{
			d.subject().hears("You're not quite sure how to begin.");
		}
		else 
		{
			d.subject().hears(spellError());
		}
		return true;
	}
	
	public String spellError()
	{
		return random(magicErrors);
	}
	
	public String spellDescription()
	{
		return "cause an object to remain exactly as it was";
	}
	
	static final String[] magicErrors = 
	{
		"You can't quite seem to remember how that one goes.",
		"Your mind feels muddled.",
		"Sparks fly from your fingertips and ... your nose goes numb for a brief moment.",
		"You can't remember what you need to do for that one, exactly."
	};
}
