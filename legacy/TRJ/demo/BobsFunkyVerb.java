package demo;
import twisted.reality.*; 

public class BobsFunkyVerb extends Verb
{
	public BobsFunkyVerb()
	{
		super("dance");
		alias("groove");
		setDefaultPrep("with");
	}

	public boolean action(Sentence d) throws RPException
	{
		Player dancer = d.subject();
		Thing dancee = d.indirectObject("with");
		Location thisRoom = d.place();

		Object[] whatOthersHear =
		{dancer, " gets down and gets funky, dancing with ", dancee, "."};
		Object[] whatBobHears =
		{"You get down, get funky, and dance around with ", dancee, "."};

		thisRoom.tellAll(dancer, whatBobHears, whatOthersHear);

		return true; 
	} 
} 
