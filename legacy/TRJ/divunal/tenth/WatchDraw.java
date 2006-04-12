package divunal.tenth;

import twisted.reality.*;

/**
 * Creates a new, blank object, with a new name and no description.<br>
 *
 * Usage: <code>&gt; draw <b>&lt;new object name&gt;</b></code>
 *
 * @version 1.0.0, 31 Jul 1999
 * @author Glyph Lefkowitz
 *
 * redone for pocketwatches by Tenth, Apr 22 1999
 */
public class WatchDraw extends Verb
{
	public WatchDraw()
	{
		super("design");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if(d.subject().isGod())
		{
			Thing th;
				
			// this is a quick hack.  Should integrate some sort
			// of "isReservedWord" checking ... where should this
			// go?
			// --glyph
			
			if ( d.directString().equals("self") || d.directString().equals("me") || d.directString().equals("here") || d.directString().equals("it") )
			{
				d.subject().hears("There is a faint metallic boinging sound from inside the watch, but nothing interesting happens.");
			}
			else
			{
				th = new Thing(d.place(),d.directString(),"It appears to be a "+d.directString()+", but it is vague, indistinct, and little more than a blurry smear on reality.");
				
				if((th.NAME()).endsWith(")"))
				{
					String n = th.NAME();
					String hertz = n.substring((n.lastIndexOf("("))+1, (n.lastIndexOf(")")));
					th.putString("name", d.directString());
					Object[] boing = {"There is an oscillating tone of about ",hertz," MHz as ",th,"'s waveform collapses."};
					d.subject().hears(boing);
				}
				
				Object[] sh = 
				{
					"You set your watch and tap the stem, and a " + d.directString() + " coalesces out space before you."
				};
				Object[] ta =
				{
					d.subject(),
					" adjusts ",
					Name.of(d.verbObject(),d.subject()),
					", and a scintillating pattern of lines billows out of space before ",
					Pronoun.obj(d.subject()),
					", coalescing into the shape of ",
					Thing.aan(d.directString()),d.directString(),"."
				};
				
				d.place().tellAll(d.subject(),sh,ta);
			}
		}
		else
		{
			Object[] dialz = {"You attempt to set a few of the dials, but pressing the button on the top produces only a faint clicking sound."};
			
			Object[] tellz = {
				 d.subject(),
				 " fumbles with the controls on the pocketwatch."
			};
			d.place().tellAll(d.subject(),dialz,tellz);
		}
		
		return true;
	}
}
