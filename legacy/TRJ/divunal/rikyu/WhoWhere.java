package divunal.rikyu;

import twisted.reality.*;
import java.util.Enumeration;

public class WhoWhere extends Verb
{
	public WhoWhere()
	{
		super("read");
		alias("open");
		alias("query");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Enumeration players = Age.theUniverse().players();
		Object[] header = {d.verbObject(), " contains the following entries:\n\nWho" + space(15) + "Where\n---------------------------------"};
		
		d.subject().hears(header);
		while(players.hasMoreElements())
		{
			Player p = (Player)players.nextElement();
			Object[] entry = {p.name(), space(18 - p.name().length()), p.topPlace() == null ? "Nowhere" : p.topPlace().NAME()};
			d.subject().hears(entry);
		}
		return true;
	}
	
	private String space(int num)
	{
		if(num < 0)
			num = 1;
		StringBuffer sb = new StringBuffer();
		for(int i = 0; i < num; i++)
		{
			sb.append(" ");
		}
		return sb.toString();
	}
}
