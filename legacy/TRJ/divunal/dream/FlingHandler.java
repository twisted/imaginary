package divunal.dream;

import twisted.reality.*;
import java.util.Random;
import java.util.Enumeration;


public class FlingHandler extends RealEventHandler
{
	public void gotEvent(RealEvent evnt, Thing thisThing)
	{
		Enumeration e = ((Room) thisThing).players();
		Random robyn = new Random();
		float f = robyn.nextFloat();
		float g = thisThing.getFloat("cloudiness");
		if ( (f < 0.5) && (g>0.0) )
		{
			g= (float) (g-robyn.nextFloat()/10);
		}
		else if (f < 0.5)
		{
			
		}
		else
		{
			g= (float) (g+robyn.nextFloat()/8);
		}
		
		if (g > 0.65)
		{
			Location lctn = (Location) thisThing.getThing("fling place");
			if ( (e != null) ? (e.hasMoreElements() && (lctn != null)) : false)
			{
				while (e.hasMoreElements())
				{
					Player p = (Player)e.nextElement();
					p.hears("The clouds roil and rise up to engulf you, gently lifting you off of your feet and pulling you somewhere else...");
					Object[] leavemsg = {
						"A tendril of smoke from the clouds envelops "
						 , p 
						 , " and spirits " 
						 , Pronoun.of(p) 
						 , " away."
					};
					Object[] entermsg = {
						 "A tendril of white smoke descends from the sky and deposits "
						 , p.name() 
						 , " on the sand."
					};
					p.moveTo((Location)thisThing.getThing("fling place"),
							 leavemsg,entermsg);
				}
			}
			g = 0;
		}
		String cloudd;
		if ( g < 0.1 )
		{
			cloudd = "The clouds are as tranquil as a lake on a cool summer's night.";
		}
		else if ( g < 0.4 )
		{
			cloudd = "The clouds look slightly turbulent.  They are swirling around in little eddies.";
		}
		else if ( g < 0.6 )
		{
			cloudd = "The clouds are very turbulent.  They are swirling and thundering quite a bit.";
		}
		else
		{
			cloudd = "The clouds are almost violent. They are spinning around rapidly, creating vortices and soft thunder everywhere.";
		}
		thisThing.putFloat("cloudiness",g);
		thisThing.putDescriptor("cloudd",cloudd);
		// keep going
		thisThing.handleDelayedEvent(new RealEvent("startup",null,null),1);
	}
}
