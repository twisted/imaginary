package divunal.magic;
import twisted.reality.*;
import java.util.Vector;

public class SpellRead extends Verb
{
	public SpellRead()
	{
		super ("read");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing spellBook=d.directObject();
		String nextSpell;
		Player sub = d.subject();
		Vector printedText=new Vector();
		int i;
		i=0;
		
		/*
		 * TODO: Insert check to make sure that the person is capable
		 * of understanding magic, and display some more
		 * confused-seeming text if they do not.
		 */ 
		
		printedText.addElement(Name.Of(spellBook));
		printedText.addElement(" has an index, consisting of many magical spells.  You leaf through the book, remembering each one for future reference:");
		nextSpell = spellBook.getString("spell "+i);
		if (nextSpell != null)
		{
			while(nextSpell != null)
			{
				i++;
				Verb v = spellBook.getVerb(nextSpell);
				if ((v != null) && (v instanceof Spell))
				{
					Spell sp = (Spell) v;
					printedText.addElement( "\nThe "+ sp.spellName() + " spell. ("+sp.spellDescription() +").");
					try
					{
						Verb vvv = sub.getAbility(sp.spellName());
						if (vvv == null)
							sub.addAbility(v.getClass().getName());
						// else if (vvv != sp)
						// I'm not sure quite what to do here...
					}
					catch (ClassNotFoundException cnfe)
					{
						Age.log("divunal panic: Loaded class not found: "+cnfe);
					}
				}
				else
				{
					if (v != null)
						printedText.addElement("\nWhat's a non-Spell ("+v+") doing on this book?");
					else
						printedText.addElement("\nWhat's a null value doing on this book?");
				}
				nextSpell = spellBook.getString("spell "+i);
			}
			Object[] ptcopy = new Object[printedText.size()];
			printedText.copyInto(ptcopy);
			Object[] leafy = {sub," intently leafs through ", spellBook, "."};			
			/*sub.hears(ptcopy);*/
			d.place().tellAll(sub,ptcopy,leafy);
		}
		else
		{
			Object[] blanks = {Name.Of(spellBook)," appears to be merely blank pages."};
			d.subject().hears(blanks);
		}
		return true;
	}
}
