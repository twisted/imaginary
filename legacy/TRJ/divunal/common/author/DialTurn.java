package divunal.common.author;
import twisted.reality.*;

public class DialTurn extends Verb
{
	public DialTurn()
	{
		super("turn");
	}

	public boolean action(Sentence d) throws RPException
	{
		Thing dial = d.directObject();
		Thing machine = d.directObject().getThing("machine");
		String towhat = d.indirectString("to");
		try
		{
			float f = Float.valueOf(towhat).floatValue();
			if ( (f <= dial.getFloat("maxval")) && (f >= dial.getFloat("minval")) )
			{
				dial.putFloat("value",f);
				Object[] youset = {"You set ",dial," to "+f+"."};
				d.subject().hears(youset);
			}
			else
			{
				d.subject().hears("No such number is on the dial.");
			}
			machine.handleEvent(new RealEvent("update",null,dial));
		}
		catch(NumberFormatException nfe)
		{
			d.subject().hears("That's not a number, you pathetic excuse for a human being.");
		}
		return true;
	}
}
