package twisted.reality.author;

import twisted.reality.*;

/**
 * <b>boolean [string : key] on [local-thing : thing] to [string : truth]</b>
 *
 * <p>Sets boolean value <i>key</i> on the thing <i>thing</i> to
 * <i>truth</i></p>
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class BoolSet extends Verb
{
	public BoolSet()
	{
		super("boolean");
		setDefaultPrep("with");
	}
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		Thing subject = d.indirectObject("on");
		String boolname = d.directString();
		boolean bool;

		if(d.hasIndirect("to"))
		{
			if (d.indirectString("to").equals("true"))
				bool=true;
			else
				bool=false;
		}
		else
			bool=false;

		subject.putBool(boolname,bool);
		d.subject().hears("Boolean set.");
			
		return true;
	}
}
