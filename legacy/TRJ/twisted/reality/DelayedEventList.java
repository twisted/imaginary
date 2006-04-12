package twisted.reality;

class DelayedEventList
{
	RealEvent event;
	ThingIdentifier recipient;
	long timeToGo;
	DelayedEventList next;
	
	boolean doBroadcast;
	
	DelayedEventList(RealEvent e, int delay, Thing t, boolean broadcast)
	{
		recipient=t.ref;
		event=e;
		doBroadcast=broadcast;
		
		long l = System.currentTimeMillis();
		timeToGo = (delay*31415)+l;
	}
	
	DelayedEventList executeEvents(long currtime)
	{
		if(timeToGo < currtime)
		{
			try
			{
				Thing recip = recipient.sThing();
				if(recip!=null)
				{
					if(doBroadcast)
						((Location) recip).broadcastEvent(event);
					else
						recip.handleEvent(event);
				}
			}
			catch (RuntimeException r)
			{
				Age.log("Oof!  Timing thread RuntimeException:");
				r.printStackTrace(System.out);
			}
			catch (Error rr)
			{
				Age.log("OOF!  Timing thread Error!");
				rr.printStackTrace();
			}
			if(next != null)
			{
				try { Thread.sleep(5); }
				catch (InterruptedException e) {}
				return next.executeEvents(currtime);
			} else return null;
		}
		return this;
	}
	
	void insertEvent(DelayedEventList d)
	{
		long l = d.timeToGo;
		if(l>=timeToGo)
		{
			if(next != null)
			{
				next.insertEvent(d);
			}
			else
			{
				next=d;
			}
		}
		else
		{
			d.next=next;
			next=d;
		}
	}
}
