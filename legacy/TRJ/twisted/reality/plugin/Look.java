package twisted.reality.plugin;

import twisted.reality.*;
import java.util.Enumeration;
import java.util.Vector;

/**
 * Makes you look at something (sets your focus on it).  Changes by
 * Bento to let you look *in* stuff, which have since been temporarily
 * disabled for being unnecessary.
 *
 * Usage: <code>&gt; look at <b>&lt;thing&gt;</b></code>
 *
 * @version 1.0.0, 15 Jun 1998
 * @author Glyph Lefkowitz */

public class Look extends Verb
{
	public Look()
	{
		super("look");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing foo=null;
		
		if(d.hasIndirect("at"))
		{
			try
			{
				foo=d.indirectObject("at");
			}
			catch (NotInterestingException nie)
			{
				d.subject().hears("There is nothing special about the "+d.indirectString("at") +".");
			}
		}
		else if (d.hasIndirect("in"))
		{
			try
			{
				foo=d.indirectObject("in");
			}
			catch (NotInterestingException nie)
			{
				d.subject().hears("There is nothing special about the "+d.indirectString("at") +".");
			}
		}
		else if (d.hasDirect())
		{
			try
			{
				foo=d.directObject();
				}
			catch(NotInterestingException nie)
			{
				Object[] nspabt = {"There is nothing special about the ",d.directString(),"."};
				d.subject().hears(nspabt);
			}
		}
		else 
		{
			foo=d.place();
		}
		if (foo != null)
		{
			d.subject().setFocus(foo);
			
			if (foo instanceof Player)
			{
				Player targetplayer = (Player) foo;
				if (targetplayer != d.subject())
				{
					Object[] xxx = {d.subject()," looks at you."};
					targetplayer.hears(xxx);
				}
			}
		}
		return true;
	}
}


/*
  It seemed like a good idea at the time, but this has all kinds of
  unwanted effects.

  if(d.hasIndirect("in")) 
  {
  Thing thi = d.indirectObject("in");
  if (thi instanceof Location)
  {
  Location c = (Location)thi;
  Vector s = new Vector();
  s.addElement(c);
  
  Enumeration e = c.things();
  if((e != null) && e.hasMoreElements())
  {
  s.addElement(" contains:");
  while(e.hasMoreElements())
  {
  Thing t = (Thing)e.nextElement();
  s.addElement("\n");
  s.addElement(t);
  }
  }
  else
  {
  s.addElement(" is completely empty.");
  }
  d.subject().hears(s);
  }
  else
  {
  // here we have an opportunity to be rude and/or
  // obnoxious to the player, for being stupid...
  Object[] peer={"You peer intently at ",thi,", but can't seem to find any openings worth looking into."};
  d.subject().hears(peer);
  //This verb is not insulting because it is a Ben Moore Patented Nice Verb (tm), Patent # 284601,225.3");
  
  }
  } */
