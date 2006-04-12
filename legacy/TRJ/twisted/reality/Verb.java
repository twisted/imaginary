package twisted.reality;

import twisted.util.LinkedList;
import java.util.Random;
/**
 * The verb class. This is the object upon which the entire action of
 * the game resides, because it is where all actions are initated.	If
 * you want to create a custom action for Twisted Reality, this is the
 * place to start looking.
 * 
 * @see Thing
 * @see Sentence
 * 
 * @version 1.0.0, 27 May 1998
 * @author Glyph Lefkowitz
 */

public abstract class Verb
{

	/**
	 * The constructor which creates a verb and names it.  You must
	 * specify the default name of the verb here which you wish to
	 * use.	 IE: the verb 'take' would have, somewhere in it, the
	 * following code:
	 *
	 * <PRE>
	 *	public Take()
	 *	{
	 *		super("take");
	 *	}
	 * </PRE>
	 *
	 * @param name The name of the verb.
	 */
	  
	protected Verb(String name)
	{
		aliases=new twisted.util.LinkedList();
		alias(name);
	}
	
	/**
	 * Adds an alias to the verb.  For instance, take can be aliased
	 * as 'get'.  Also (and not quite so obviously), a verb light
	 * 'turn' for a lamp, as in 'turn on' or 'turn off' can be
	 * aliased to something creative like 'light' and 'unlight' so
	 * you can type 'turn on lamp' 'turn off lamp' 'light lamp'
	 * etc. This will require being clever with how you locate the
	 * lamp in the verb though.
	 *
	 * @param othername The additional name of the verb.
	 */
	
	public void alias(String othername)
	{
		if (othername != null)
			aliases.addElement(othername.toLowerCase());
	}
	
	String defaultPrep;
	
	/**
	 * This sets the "default preposition" of a verb.  Call this in a
	 * verb's constructor if you want the verb to be attached to an
	 * object, but still "automatic", I.E.: if you're writing
	 * weird.game.FishingVerb that calls setDefaultPrep("with");, and
	 * you enable that verb on a fishing pole, a player typing "fish"
	 * would see: "$ fish (with the fishing pole)" and stuff would
	 * happen.	This is not always the desired behavior, but for
	 * frequently used actions it can be very convenient.
	 *
	 * @param prep The preposition requested to be default
	 */
	
	public void setDefaultPrep(String prep)
	{
		defaultPrep=prep;
	}
	
	/**
	 * This sets the "default preposition" of a verb so that the
	 * default preposition is "direct object" (and not any actual
	 * preposition).
	 *
	 * @see setDefaultPrep
	 */
	
	public void setDefault()
	{
		setDefaultPrep("");
	}
	
	/**
	 * This is the function you must override to give the verb
	 * meaning.	 It is here that you create anything that the verb
	 * actually <b>does</b>.
	 * 
	 * @param descriptor The sentence which contains information about
	 * how the verb was executed.
	 */
	public abstract boolean action(Sentence descriptor) throws RPException;

	twisted.util.LinkedList aliases;
	
	static Random rand = new Random();
	
	/**
	 * This returns a random integer (it might be any int value, positive or negative).
	 */
	
	public static int random()
	{
		return rand.nextInt();
	}
	
	/**
	 * This returns a random float (from 0-1).
	 */
	
	public static float randomf()
	{
		return rand.nextFloat();
	}
	
	/**
	 * Do not call this function.  Ever.  It doesn't do anything.
	 */
	
	public static void randomize()
	{
		rand=new Random();
		Age.log("rerandomizing Verb. Why??");
	}
	
	/**
	 * This is a utility function for grabbing a random string from a
	 * list.  Given an array of strings, it will return some random
	 * element of that list.
	 * 
	 * @param stringList a long list of strings from which to choose a
	 * random option.
	 */
	
	public static String random(String[] stringList)
	{
		return stringList[Math.abs(random())%stringList.length];
	}
}
