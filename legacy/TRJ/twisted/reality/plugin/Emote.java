package twisted.reality.plugin;
import twisted.reality.*;

/**
 * Emote will emote an action, a feature used by freeform roleplayers.
 * You may tap the ';' key as a shortcut. All emotes appear with a "*"
 * at the beginning of the line, so that roleplaying can be
 * distinguished from "reality", preventing people from abusing the
 * emote command to create illusions.
 *
 * Usage: <code>&gt; emote <b>"&lt;phrase&gt;</b>"</code>
 *
 * @version 1.0.0, 15 Jun 1998
 * @author Glyph Lefkowitz */

public class Emote extends Verb
{
	public Emote()
	{
		super("emote");
	}
	public boolean action(Sentence d) throws RPException
	{
	   String q = d.directString();
	   if(!(q.endsWith(".")||q.endsWith("!")||q.endsWith("?")||q.endsWith("\"")))
	   {
		  q+=".";
	   }
	   if(!(q.startsWith("'") || q.startsWith(" ")))
	   {
		  q=" "+q;
	   }
	   
	   d.place().tellEverybody("* "+d.subject().name() + q);
	   return true;
	}
}
