package twisted.reality.author;

import twisted.reality.*;

/**
 * <b>gate [new-portal : direction] to [global-room : room] </b>
 * <p>Opens a temporary one-way door in the direction specified, leading
 * to room.  The gate lasts for about 30 seconds, and is visible to
 * players as a swirling blue effect similar to the twisted reality
 * logo. Note that there must not already be an exit in the direction
 * that the gate is going to be placed.</p>
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Gate extends Verb
{
	public Gate()
	{
		super("gate");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		if( d.place().getBool("gate active") )
		{
			d.subject().hears("Yow!... this room's reality is already too warped.  Wait a little while.");
		}
		else
		{
			Room myrm = (Room) d.place();
			if(myrm.getPortal(d.directString())==null)
			{
				Thing t=Age.theUniverse().findThing(d.indirectString("to"));
				
				if(t!=null)
				{
					if(t instanceof Room)
					{
						Room r = (Room) t;
						try {
							myrm.putHandler("gate","twisted.reality.author.GateExitKillHandler");
						} catch (ClassNotFoundException e) {
							d.subject().hears("Internal Error with Gate.");
							Age.log("Error adding GateExitKillHandler: " + e);
							return true;
						}
						myrm.addPortal(new Portal(myrm,r,d.directString()));
						d.subject().respond("Your mind quests outward to the place you seek, and a Gate opens before you.");
						myrm.tellEverybodyBut(d.subject(),"There is a sound of fabric rending.  "+d.directString()+"ward, a Gate opens.");
						
						myrm.putBool("gate active",true);
						
						String[] x = new String[2];
						
						
						
						x[0]=d.directString();
						x[1]="gated";
						
						myrm.handleDelayedEvent(new RealEvent("gate",x,myrm),3);
						myrm.putDescriptor(x[1]," To the "+d.directString()+", a swirling mass of air surrounds an unstable magic portal.");
					}
					else
					{
						myrm.tellEverybody("A gate begins to open - but it is unstable, and small, and collapses."); 
					}
				}
				else
				{
					d.subject().hears("You cannot open a gate to nowhere.");
				}
			}
			else
			{
				d.subject().hears("A force pushes your mind back - you cannot create a Gate there.");
			}
		}
		return true;
	}
}
