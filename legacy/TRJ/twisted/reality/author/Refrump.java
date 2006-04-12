package twisted.reality.author;
import twisted.reality.*;

public class Refrump extends Verb
{
	public Refrump()
	{
		super("refrump");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Age.theUniverse().reloadEverything();
		d.subject().hears("Ka-chunk.");
		return true;
	}
}
