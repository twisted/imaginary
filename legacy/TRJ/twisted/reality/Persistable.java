package twisted.reality;

/**
 * If you want to store a persistable data-type, use this class.  You
 * will need to override methods to create a string from it and
 * recreate the object.  Only fairly expert programmers should attempt
 * to do this, as it's pretty much the only programming error
 * (game-developer wise) that can cause Twisted Reality to fail to
 * persist the map.
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public interface Persistable
{
	/**
	 * Called to initialize your Persistable when it's being created
	 * from a String.  (Note: although the Java language allows no
	 * syntactic method to enforce this, you must provide a public
	 * constructor with no arguments to allow for instantiation of
	 * your class in this manner.)
	 */
	void fromString(String s) throws java.io.IOException;
	
	/**
	 * Called to convert the object back into a string
	 */
	String persistance();
}
