package twisted.reality;

/**
 * This class is an eventhandler.  In order to handle an event, you
 * must override this class and add it to an object in the game (most
 * likely with the "handle" authoring verb).  Event handlers come in
 * all shapes and sizes, but the simplest example is that of an attack
 * - when you attack someone, writing the attack code straight into
 * the verb would be simple... but what about a person who has
 * 6-foot-thick armor on?  Your attack, and thusly your verb, would be
 * the same, but their response to that action would definitely be
 * different.  You would send an "attack" event from somewhere, and
 * then Mister Armor Guy would recieve this event and have a handler
 * for it different from the standard Player "attack" event handler.
 *
 * In short, this allows for verbs to handle stuff with greater
 * versatility and less code.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public abstract class RealEventHandler
{
	/**
	 * This is the method you must override to give your eventhandler
	 * meaning.
	 *
	 * @param e The event to be handled
	 * @param thisThing The thing that the event is being handled on.
	 */
	
	public abstract void gotEvent(RealEvent e, Thing thisThing);
	
	/**
	 * This is exactly the same as Verb.random(), included here for
	 * convenience's sake.
	 *
	 * @see twisted.reality.Verb
	 */
	
	public static int random()
	{
		return Verb.random();
	}
	
	/**
	 * This is exactly the same as Verb.randomf(), included here for
	 * convenience's sake.
	 * 
	 * @see twisted.reality.Verb
	 */
	
	public static float randomf()
	{
		return Verb.randomf();
	}
	
	/**
	 * This is exactly the same as Verb.random(String[]), included
	 * here for convenience's sake.
	 *
	 * @see twisted.reality.Verb
	 */
	
	public String random(String[] stuff)
	{
		return Verb.random(stuff);
	}
}
