package twisted.reality.author;

import twisted.reality.*;

/** 
 * This is a utility function for the creators of the game, or others
 * with a high degree of familiarity with the '.por' file format.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Sketch extends Verb
{
	public Sketch()
	{
		super("sketch");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		d.subject().requestResponse(
									new SketchProcessor(d.subject())
									,
									"Sketching "+d.directString()
									,(d.hasDirectObject()) ? (d.directObject().persistance()) :
									("Thing\n{\n\tname \""+d.directString()+"\"\n\tplace \""+d.place().name()+
									 "\"\n\tdescribe \"A blue box.\"\n}")
									);
		
		return true;
	}
}
