package divunal.dream;

import twisted.reality.*;

public class FlowerSmell extends Verb
{
	public FlowerSmell()
	{
		super("smell");
		alias("sniff");
	}
	public boolean action(Sentence d) throws RPException
	{
		Object[] ts = {"You smell the flowers, you close your eyes.  As the cool, pleasant smell of frozen roses pervades your senses, you can see the outline of a snowflake against the back of your eyelids."};
		Object[] teb =
		{
			d.subject(), " presses ", Name.of("face",d.subject())," into the flowers, inhales deeply, and looks content."
		};
		d.place().tellAll(d.subject(),ts,teb);
		return true;
	}
}
