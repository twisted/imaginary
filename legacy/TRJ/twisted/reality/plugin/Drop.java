package twisted.reality.plugin;

import twisted.reality.*;

/**
 * Drop drops an object.  If you're holding it, you no longer will
 * be.<br>
 *
 * Usage: <code>&gt; drop <b>&lt;thing&gt;</b></code>
 *
 * @version 1.0.0, Jun 13 1999
 * @author Glyph Lefkowitz
 */

public class Drop extends Verb
{
	public Drop()
	{
		super("drop");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player prp = d.subject();
		if(d.hasDirectObject()) 
		{
			Thing tt;
			try
			{
				tt = d.directObject();
			}
			catch(AmbiguousException ae)
			{
				tt = TRUtils.reduceAmbiguity(ae,prp,new TRUtils.IsIn(prp));
			}
			if(tt.place()==prp)
			{
				
				Object[] tmps = {prp," drops ",tt,"."};
				if(tt.moveTo(d.place(), tmps,tmps ))
					prp.hears(tt.nameTo(prp) + ": dropped.");
				else
					prp.hears("Oh dear, it's stuck to you!");
			}
			else
			{
				prp.hears("You don't have one of those.");
			}
		}
		else
		{
			prp.hears("You don't have one of those.");
		}
		return true;
	}
}
