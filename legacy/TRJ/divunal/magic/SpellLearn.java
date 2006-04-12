package divunal.magic;
import twisted.reality.*;

public class SpellLearn extends Verb
{
	public SpellLearn()
	{
		super("learn");
		alias("study");
		setDefaultPrep("from");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		String spellToLearn=d.directString();
		Thing spellBook=d.indirectObject("from");
		Verb spellVerb = spellBook.getVerb(spellToLearn);
		
		/*
		 * TODO: insert check to make sure a person knows how to
		 * comprehend magic, and if they don't, don't allow them to
		 * study, or even know that they *can* study from this book
		 */
		
		if ((spellVerb != null) && (spellVerb instanceof Spell))
		{
			Spell spel = ((Spell) spellVerb);
			String spnm = spel.spellName();
			String spelern = "learned " + spnm;
			
			Player student = d.subject();
			int totalspells = student.getInt("spells learned");
			int spells = student.getInt(spelern);
			
			/* TODO: make this computed off of your stats.  Memory, I
			 * think, for this form of magic, considering this is a
			 * "learn" verb, after all.  Memory is the best stat in
			 * the game.
			 */
			
			int hardmax = 6;
			
			if (totalspells >= hardmax)
			{
				student.hears("You can't seem to memorize another spell.  You've got too much buzzing around in there already.");
			}
			else
			{
				Object[] youStudy = {"You diligently study " + spnm + " until you have committed it to memory."};
				
				Object[] theyStudy = {student," reads dilligently from ",Name.of(spellBook,student),"."};
				d.place().tellAll(student,youStudy,theyStudy);
				totalspells++;
				spells++;
				if (spells == 0) spells++;
				student.putInt(spelern,spells);
				student.putInt("spells learned",totalspells);
			}
		}
		else
		{
			Object[] doesntSay={spellBook," doesn't say anything about that."};
			d.subject().hears(doesntSay);
		}
		return true;
	}
}
