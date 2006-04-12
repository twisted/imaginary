package twisted.reality.client;

import twisted.util.KeyFilterEnumeration;

import java.util.*;


public class ThingList
{
	class ThingEnumeration extends KeyFilterEnumeration
	{
		/* h from enclosing class really SHOULD be accessable, but it doesn't work right */
		public ThingEnumeration(Hashtable h)
		{
			super(h.keys(),h.elements());
		}
		public boolean filterKey(Object o)
		{
			return (!h.containsKey("+"+o));
		}
	}
	
	Hashtable h=new Hashtable();
	
	class ThingEnterRun extends Thread
	{
		public ThingEnterRun(String ithing, String imessage)
		{
			thing = ithing;
			message = imessage;
			start();
		}
		public void run()
		{
			h.remove("-"+thing);
			h.put("+"+thing,"+++ <"+message+">");
			fireListChanged();
			try{ Thread.sleep(8000); } catch (Exception e) {}
			h.remove("+"+thing);
			fireListChanged();
		}
		String thing;
		String message;
	}
	
	class ThingLeaveRun extends Thread
	{
		public ThingLeaveRun(String ithing, String imessage)
		{
			thing = ithing;
			message = imessage;
			start();
		}
		
		public void run()
		{
			h.remove("+"+thing);
			h.put("-"+thing,"--- ("+message+")");
			fireListChanged();
			try{ Thread.sleep(8000); } catch (InterruptedException e) {}
			h.remove("-"+thing);
			fireListChanged();
		}

		String thing;
		String message;
	}
	
	public void putAdd(String add, String desc)
	{
		new ThingEnterRun(add,desc);
	}
	
	public void putRem(String rem, String desc)
	{
		new ThingLeaveRun(rem,desc);
	}
	
	public void remove(String rem)
	{
		h.remove(rem);
		fireListChanged();
	}
	
	public void putThing(String name, String desc)
	{
		h.remove("-"+name);
		h.put(name,desc);
		fireListChanged();
	}
	
	public Enumeration elements()
	{
		return new ThingEnumeration (h);
	}

	ListListener mll;
	
	public void setListListener(ListListener ll)
	{
		mll=ll;
		fireListChanged();
	}
	
	public void fireListChanged()
	{
		if (mll!=null)
			mll.listUpdated(this);
	}
}
