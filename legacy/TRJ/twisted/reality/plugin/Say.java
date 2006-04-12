package twisted.reality.plugin;
import twisted.reality.*;

/**
 * The 'say' verb.  This makes your character say one quoted
 * string, as in
 * <P><Blockquote><TT>Bob says "Hello."</TT></Blockquote></P>
 *
 * Usage: say "string"
 *
 * @version 1.0.0, 15 Jun 1998
 * @author Glyph Lefkowitz
 */

public class Say extends Verb
{
	public Say()
	{
		super ("say");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		RealEvent r = new RealEvent("say",d.directString(),d.subject());
		
		d.place().broadcastEvent(r);
		d.subject().broadcastEvent(r);
		
		return true;
	}
}
