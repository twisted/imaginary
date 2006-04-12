package twisted.reality;
import java.io.*;
import twisted.util.*;
/**
 * This class generates ThingFactories for parsing data from files.
 * This can be used when writing verbs to create objects from template
 * text-files or munged input from the user.
 * 
 * @see twisted.reality.author.Sketch
 */
class FactoryFactory
{
	private FactoryFactory()
	{
		// not publicly instantiatable
	}
	/**
	 * Generate a ThingFactory
	 *
	 * @param s The name of the class to generate a factory for.
	 * @param st The string tokenizer to tokenize from
	 * @param w The wrapper which will be executed to verify this object.
	 */	
	public static final ThingFactory getFactory(String s, StreamTokenizer st, SetupWrapper w)
	{
		if (s.equals("Thing"))
		{
			return new ThingFactory(st,w);
		}
		else if (s.equals("Room"))
		{
			return new RoomFactory(st,w);
		}
		else if (s.equals("Player"))
		{
			return new PlayerFactory(st,w);
		}
		else if (s.equals("Location"))
		{
			return new LocationFactory(st,w);
		}
		else if (s.equals("class"))
		{
			return new MetaThingFactory(st,w);
		}
		
		return null;
	}
}
