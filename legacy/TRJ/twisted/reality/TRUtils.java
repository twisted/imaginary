package twisted.reality;

import java.util.Enumeration;

public class TRUtils
{
	/**
	 * This class may not be constructed.  It is for static utilities
	 * only.  */
	private TRUtils() {}

	/**
	 * This interface is a placeholder for passing code to ReduceAmbiguity.
	 */
	
	public interface Validator
	{
		boolean valid(Thing t);
	}
	public static class IsIn implements Validator
	{
		Location myl;
		public IsIn(Location l)
		{
			myl=l;
		}
		public boolean valid(Thing t)
		{
			/**
			   Location mnl = t.place();
			   while(mnl!=null)
			   {
			   if (myl==mnl) return true;
			   mnl=mnl.place();
			   }
			*/
			return t.place()==myl;
		}
	}
	
	public static class Not implements Validator
	{
		Validator myv;
		public Not(Validator v)
		{
			myv = v;
		}
		public boolean valid(Thing t)
		{
			return !myv.valid(t);
		}
	}

	/**
	 * This is for verbs which know that they only could be referring
	 * to objects who meet a certain condition.  Take and drop, for
	 * example, know that they only want objects that are either in
	 * the floor or in the room.
	 */

	public static Thing reduceAmbiguity(AmbiguousException ae,
										Player plr,
										Validator vdr)
		throws AmbiguousException
	{
		Enumeration aee = ae.elements();
		twisted.util.LinkedList lnk = new twisted.util.LinkedList();
		Thing elm=null;
		while(aee.hasMoreElements())
		{
			elm = (Thing) aee.nextElement();
			if (vdr.valid(elm))
			{
				lnk.addElement(elm);
			}
		}
		if (lnk.size()==1)
		{
			return elm;
		}
		else
		{
			throw new AmbiguousException(lnk.elements(),ae.s,plr);
		}
	}
}
