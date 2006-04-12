package twisted.reality.author;

import twisted.reality.*;

/**
 * This verb is a utility for undescribing description elements.  If
 * you accidentally add one in a Verb or eventhandler and want to
 * manually remove it, "undescript KEY on THING" should fix it.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */
public class DescriptSet extends twisted.reality.Verb
{
	public DescriptSet()
	{
		super("descript");
		alias("undescript");
	}
	
	public boolean action (twisted.reality.Sentence d) throws twisted.reality.RPException
	{
		if (!d.subject().isGod()) return false;

		Player p = d.subject();
		Thing target = d.indirectObject("on");
		String elementName = d.directString();
		Location l = p.place();

		if (d.verbString().equals("undescript"))
		{
			target.removeDescriptor(elementName);
			Object[] pRemoves = {"Descriptive Element \"",elementName,"\" removed. (Since there is currently no way to confirm that there was an element called \"",elementName,"\", you might want to check on that."};
			Object[] oRemoves = {p," stares intently at ",target," as details swirl off of ",Pronoun.obj(target)," into nothing."};
			l.tellAll(p, pRemoves, oRemoves);
			return true;
		}
		else
		{
			String element = d.indirectString("to");
			target.putDescriptor(elementName, element);
			Object[] pAdds = {"Descriptive element added."};
			Object[] oAdds = {p," stares intently at ",target," as a swirl of change surrounds ",Pronoun.obj(target),"."};

			l.tellAll(p, pAdds, oAdds);
			return true;
		}
	}
}
