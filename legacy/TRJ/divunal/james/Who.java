package divunal.james;
import twisted.reality.*;
import java.util.Enumeration;
import twisted.util.StringUtilities;

public class Who extends Verb
{
	public Who()
	{
		super("who");
	}
	public boolean action(Sentence d) throws RPException
	{
		Player to = d.subject();
		Enumeration e = Age.theUniverse().players();
		while(e.hasMoreElements())
		{
			Player p = (Player)e.nextElement();
			to.hears(StringUtilities.pad(p.name(), 30) + ((p.place() != null)?p.place().name():"(nowhere)"));
		}
		return true;
	}
}
