package divunal.damien;

import twisted.reality.*;

/** NOT FIXED FOR PERSPECTIVES **/

public class Gate extends Verb
{
	public Gate()
	{
		super("gate");
	}
	
	public boolean action(Sentence d) throws RPException
	{  
		if(d.place() instanceof Room)
		{
			Room rm = (Room) d.place();
			if(rm.getPortal(d.directString())==null)
			{
				Thing t=Age.theUniverse().findThing(d.indirectString("to"));
				if(t!=null)
				{
					if(t instanceof Room)
					{
						Room r = (Room) t;
						rm.addPortal(new Portal(rm,r,d.directString()));
						d.subject().respond("With a few deft strokes of your pen, you alter the bit in the Contract about gateways not being there. Now, a gateway is here.");
						rm.tellEverybodyBut(d.subject(),"A quiet knock sounds "+d.directString()+"ward, and a small wooden door appears..");
						
						try {
						rm.putHandler("gate","twisted.reality.author.GateExitKillHandler");
						} catch (ClassNotFoundException cnfe) {
							d.subject().hears("Nothing Happens Here.");
							return true;
						}
						
						String[] x = new String[2];
						
						x[0]=d.directString();
						x[1]="gated";
						
						d.place().handleDelayedEvent(new RealEvent("gate",x,d.place()),3);
						d.place().putDescriptor(x[1],"To the "+d.directString()+", is a small wooden door marked `Private'. It shimmers in the air like heat from a fireplace.");
					}
					else
					{
						d.place().tellEverybody("A gate begins to open - but it is unstable, and small, and collapses."); 
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
		else
		{
			d.subject().hears("This place is too small for that.");
		}
		return true;
	}
}
