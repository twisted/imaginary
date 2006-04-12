package twisted.reality.author;
import twisted.reality.*;

/**
 * Specify that an event should be handled by a particular handler.
 * This is to construct complex Things at runtime. <br>
 *
 * Usage: <code>&gt; handle <b>&lt;event name&gt;</b> on
 * <b>&lt;thing&gt;</b> with <b>&lt;handler classname&gt;</b></code>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Handle extends Verb
{
	public Handle()
	{
		super("handle");
		alias("unhandle");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		if(d.verbString().equals("handle"))
		{
			String eventToHandle = d.directString();
			String classToLoad = d.withString();
			Thing thingToUse = d.indirectObject("on");
			
			try
			{
				thingToUse.putHandler(eventToHandle,classToLoad);
				d.subject().hears("Handler loaded.");
			}
			catch (ClassNotFoundException e)
			{
				d.subject().hears("Load failed:" + e);
			}
		}
		else
		{
			String eventNotToHandle = d.directString();
			Thing thingToUse = d.indirectObject("on");
			thingToUse.removeHandler(eventNotToHandle);
			d.subject().hears("Handler removed.");
		}
		
		return true;
	}
}
