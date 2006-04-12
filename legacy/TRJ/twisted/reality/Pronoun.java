package twisted.reality;

import twisted.util.StringLegalizer;

/**
 * This is a class which represents a pronoun -- him, her, he, she, it
 * etcetera.  This is a post-processed version which will be
 * interpreted for each player, rather than being the same for
 * everyone (in case an object appears to be male to one player and
 * female to another.)
 */

public class Pronoun implements Perceptible
{
	Pronoun (ThingIdentifier t, int flag)
	{
		ref=t;
		mflag=flag;
	}
	
	/**
	 * Generates a new pronoun from t.  'Flag' can be one of the
	 * constant values himher, HIMHER, heshe, or HESHE.
	 */
	
	public Pronoun(Thing t, int flag)
	{
		this(t.ref,flag);
	}
	int mflag;
	
	/**
	 * Returns the map persistence of this Pronoun.  This will look
	 * something like {Pronoun of("foo")}.
	 */
	
	public String toString()
	{
		StringBuffer sbr = new StringBuffer("Pronoun ");
		String sp;
		switch (mflag)
		{
		case himher:
			sp="obj";
			break;
		case heshe:
			sp="of";
			break;
		case hisher:
			sp="pos";
			break;
		case HIMHER:
			sp="Obj";
			break;
		case HESHE:
			sp="Of";
			break;
		case HISHER:
			sp="Pos";
			break;
		default:
			sp="of";
		}
		sbr.append(sp);
		
		sbr.append("(\"");
		sbr.append(StringLegalizer.legalize(ref.sThing().NAME()));
		sbr.append("\")");
		return sbr.toString();
	}
	
	/**
	 * Returns the way this pronoun will look to a certain object.
	 */
	
	public String toStringTo(Thing t)
	{
		switch(mflag)
		{
		case himher:
			return ref.sThing().himher();
		case heshe:
			return ref.sThing().heshe();
		case hisher:
			return ref.sThing().hisher();
		case HIMHER:
			return ref.sThing().HimHer();
		case HESHE:
			return ref.sThing().HeShe();
		case HISHER:
			return ref.sThing().HisHer();
		default:
			return null;
		}
	}
	
	/**
	 * Returns the Thing that this Pronoun represents.
	 */
	
	public Thing getThing()
	{
		return ref.sThing();
	}
	
	public static final int CAPS=1;
	
	/**
	 * A constant representing the string "him" "her" or "it"
	 */
	public static final int himher=0;
	/**
	 * A constant representing the string "Him" "Her" or "It".
	 */
	public static final int HIMHER=himher|CAPS;
	/**
	 * A constant representing the string "he" "she" or "it".
	 */
	public static final int heshe=2;
	/**
	 * A constant representing the string "He" "She" or "It".
	 */
	public static final int HESHE=heshe|CAPS;
	
	public static final int hisher=4;

	public static final int HISHER=hisher|CAPS;
	
	ThingIdentifier ref;
	boolean caps;
	
	/**
	 * Returns a Object encapsulating the pronoun of the Thing 'toName'.
	 * If the pronoun is not dynamic, this returns a static string, otherwise,
	 * it returns a Perceptible.
	 */
	public static Object of(Thing toName)
	{
		return new Pronoun(toName.ref, heshe);
	}
	
	/**
	 * Returns a Object encapsulating the pronoun of the Thing
	 * 'toName' with initial caps.  If the pronoun is not dynamic,
	 * this returns a static string, otherwise, it returns a
	 * Perceptible.
	 */
	
	public static Object Of(Thing toName)
	{
		return new Pronoun(toName.ref, HESHE);
	}
	
	/**
	 * Returns the object pronoun (him, her or it) of the given Thing.
	 */

	public static Object obj(Thing toName)
	{
		return new Pronoun(toName.ref,himher);
	}
	
	/**
	 * Returns the object pronoun (Him, Her or It) of the given Thing.
	 */
	
	public static Object Obj(Thing toName)
	{
		return new Pronoun(toName.ref,HIMHER);
	}
	/**
	 * Returns the posessive pronoun (his, her or its) of the given Thing.
	 */

	public static Object pos(Thing toName)
	{
		return new Pronoun(toName.ref,hisher);
	}
	
	/**
	 * Returns the object pronoun (His, Her or Its) of the given Thing.
	 */
	
	public static Object Pos(Thing toName)
	{
		return new Pronoun(toName.ref,HISHER);
	}
}
