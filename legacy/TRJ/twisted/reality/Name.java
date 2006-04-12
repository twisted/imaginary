package twisted.reality;

import twisted.util.StringLegalizer;

/**
 * This class implements the Perceptible interface to
 * return a name appropriate for the Player viewing the
 * object its created for.
 */
public class Name implements Perceptible
{
	Name(ThingIdentifier t, ThingIdentifier owner, boolean capsd)
	{
		ref=t;
		posessor=owner;
		caps=capsd;
	}
	
	/**
	 * Constructs a new Name for a Thing *t* which is owned by
	 * (preceeded by the posessive pronoun for) *owner*.
	 * 
	 * @param caps Is this name capitalized?
	 */
	
	public Name(Thing t, Thing owner, boolean caps)
	{
		this(t.ref,owner.ref,caps);
	}
	
	/**
	 * Returns the way this Name looks to a particular Thing.
	 */
	
	public String toStringTo(Thing t)
	{
		String ntt = ref.sThing().nameTo(t);
		if (posessor == null)
		{
			return (caps?ref.sThing().The():ref.sThing().the())+ntt;
		}
		else if (t == posessor.sThing())
		{
			return (caps?"Your ":"your ")+ntt;
		}
		else if (posessor.sThing() == ref.sThing())
		{
			return (caps?posessor.sThing().HimHer():posessor.sThing().himher())+"self";
		}
		else
		{
			return (caps?posessor.sThing().HisHer():posessor.sThing().hisher())+" "+ntt;
		}
	}
	
	/**
	 * Returns the persistance of this Name. This is typically
	 * something you don't want to deal with within the game -- this
	 * is intended to aid in debugging.
	 */
	
	public String toString()
	{
		StringBuffer myFin = new StringBuffer("Name ");
		
		if (caps)
			myFin.append("Of(");
		else
			myFin.append("of(");
		
		if (ref!=null&&ref.sThing() != null)
		{
			myFin.append("\"");
			myFin.append(StringLegalizer.legalize(ref.sThing().NAME()));
			myFin.append("\"");
		}
		
		if (posessor!=null&&posessor.sThing()!=null)
		{
			myFin.append(",\"");
			myFin.append(StringLegalizer.legalize(posessor.sThing().NAME()));
			myFin.append("\"");
		}
		
		myFin.append(")");
		return myFin.toString();
	}
	
	/**
	 * Returns the Thing that this Name represents.
	 */
	
	public Thing getThing()
	{
		return ref.sThing();
	}
	
	ThingIdentifier ref;
	boolean caps;
	ThingIdentifier posessor;
	
	/**
	 * Returns a Object encapsulating the name of the Thing 'toName'.
	 */
	
	public static Object of(Thing toName)
	{
		return new Name(toName.ref,null,false);
	}
	
	/**
	 * Returns a Object encapsulating the name of the Thing 'toName'
	 * with initial caps.
	 */

	public static Object Of(Thing toName)
	{
		return new Name(toName.ref,null,true);
	}
	/**
	 * Returns a Perceptible encapsulating the name of the Thing 'toName'
	 * with Thing (usu. Player) owner as the owner (this person sees
	 * 'Your white box' and everyone else sees 'his/her white box'
	 * as opposed to everyone seeing 'The white box').
	 */
	public static Object of(Thing toName, Thing owner)
	{
		return new Name(toName.ref,owner.ref,false);
	}
	
	/**
	 * his (or her) toName.
	 */
	
	public static Object of(String toName, Thing owner)
	{
		return owner.hisher()+" "+toName;
	}
	
	/**
	 * His (or Her) toName.
	 */
	
	public static Object Of(String toName, Thing owner)
	{
		return owner.HisHer()+" "+toName;
	}
	
	/**
	 * Returns a Perceptible encapsulating the name of the Thing
	 * 'toName' with initial caps, and with Thing (usu. Player) owner
	 * as the owner. (see above)
	 */
	
	public static Object Of(Thing toName, Thing owner)
	{
		return new Name(toName.ref,owner.ref,true);
	}
}
