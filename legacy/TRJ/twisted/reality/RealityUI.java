package twisted.reality;
import java.util.*;


abstract class RealityUI implements Runnable
{
	abstract void hears(String aPhrase);
	
	void notifyMoved()
	{
		Location l = myPlayer.place();
		while ( (l!=null) && (l.isBroadcast()) )
			l=l.place();
		myPlayer.setFocus(l);
		
	}
	void notifyDescriptRemove(String theKey)
	{
	}
	
	long askedWait=0;
	int waitFor=0;
	
	protected void startThread()
	{
		t=new Thread(this);
		t.start();
	}
	
	Thread getThread()
	{
		return t;
	}
	
	Thread t;
	
	/**
	 * subclasses must call this somewhere in their input loop 
	 *
	 * This is done this way because puppeting people ought not to delay you.
	 */
	void delayAndExecute(String toExecute)
	{
		long now = System.currentTimeMillis();
		if (askedWait != 0 && waitFor != 0)
		{
			int alreadyWaited = (int) (now-askedWait);
			int reallyWaitFor =  waitFor-alreadyWaited;
			
			askedWait=0;
			waitFor=0;
			if (reallyWaitFor>0)
			{
				hears("You can't do that right now.");
				try
				{
					Thread.sleep(reallyWaitFor);
				}
				catch(InterruptedException inter)
				{
					Age.log("I just got an InterruptedException ("+inter+") in RealityUI.delayAndExecute().  Does this ever really happen?");
				}

				return;
			}
		}
		myPlayer.execute(toExecute);
	}
	
	RealityUI()
	{
	}
	
	void theme(String st)
	{
	}
	
	void notifyLeaving(Thing th, Thing inth, String str)
	{
	}
	
	void notifyEntering(Thing th, Thing inth, String str)
	{
		
	}
	
	void requestResponse(Long l,String s,String r)
	{
	}
	
	void notifyEntered(Thing th, Thing inth)
	{
	}
	
	void notifyLeft(Thing th, Thing inth)
	{
	}
	
	void notifyDescriptAppend(String data, String foo)
	{
	}
	
	void attachToPlayer(Player inPlayer)
	{
		if ((inPlayer == null) && (myPlayer != null))
			dispose();
		myPlayer = inPlayer;
	}
	
	Player who()
	{
		return myPlayer;
	}
	
	void errorMessage(String message)
	{
		hears(message);
	}

	void startCX(CXHandler c)
	{
		throw new RealClientException("CX unsupported");
	}
	
	boolean clientSupportsCX(String cx)
	{
		return false;
	}

	void sendCXData(Object cxnum, String message)
	{
		throw new RealClientException("CX unsupported");
	}
	
	void sendCXData(Object cxnum, Object[] message)
	{
		throw new RealClientException("CX unsupported");
	}
	
	void stopCX(Object cxnum)
	{
		throw new RealClientException("CX unsupported");
	}
	
	abstract void setFocus(Thing th);
	
	/**
	 * This is for cleaning up native stuff like networking or
	 * graphics contexts
	 */
	void dispose() {}

	protected Player myPlayer;
}
