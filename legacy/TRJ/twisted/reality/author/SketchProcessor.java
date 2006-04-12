package twisted.reality.author;

import twisted.reality.*;
import twisted.util.*;
import java.io.StringReader;
import java.io.StreamTokenizer;
import java.util.Enumeration;
import java.io.IOException;

/**
 * This is a processor for the verb Sketch.
 *
 * @see Sketch
 *
 * @version 1.0.1, 13 Aug 1999
 * @author Glyph Lefkowitz
 */

public class SketchProcessor implements ResponseProcessor
{
	public SketchProcessor(Player p)
	{
		pl=p;
	}
	public void gotResponse(String s)
	{
		pl.hears("Starting parse.");
		try
		{
			Age.theUniverse().loadMapString(s);
		}
		catch (IOException e)
		{
			pl.hears("Input-output exception.");
		}
		catch (RPException rpe)
		{
			pl.hears(rpe.toString());
		}
	}
	
	Player pl;
}
