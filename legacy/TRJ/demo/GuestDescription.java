package demo;

import twisted.reality.*;
import java.util.Vector;

public class GuestDescription extends DynamicProperty
{
	public Object value(Thing o, Thing d)
	{
		Vector description=new Vector();
		String adjective = o.getString("adjective");
		String genderPronoun = o.getString("gender pronoun");

		description.addElement("A strangely generic "+genderPronoun+", with a certain distinguishing "+adjective+" quality to ");
		description.addElement(Pronoun.obj(o));
		description.addElement(".");
		
		if (!(o.name().endsWith("Guest")))
		{
			description.addElement(" The lack of individuality seems to be due mostly to ");

			description.addElement(Pronoun.obj(o));
			description.addElement(" being a guest, though, since ");
			description.addElement(Pronoun.of(o));
			description.addElement(" actually has a name.");
		}
		return o.fromVector(description);
	}
}
