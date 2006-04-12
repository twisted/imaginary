package twisted.reality;

/**
 * This interface is used to make dynamic elements of a string.
 * If you pass a Perceptible in the Object[] passed to Player.hears
 * or Thing.tellAll, it will evaluate it with the appropriate Thing
 * as the target. This allows e.g. a Thing's name to look different to
 * each player. You can of course override it to return whatever dynamic
 * string you wish.
 * 
 * @see twisted.reality.Name
 * 
 * @see twisted.reality.Pronoun
 */
public interface Perceptible
{
	String toStringTo(Thing t);
	// Why was this here to begin with???
	// Thing getThing();
}
