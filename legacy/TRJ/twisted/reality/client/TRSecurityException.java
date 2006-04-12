package twisted.reality.client;

/**
 * Signals that a security exception has occurred.
 */
public class TRSecurityException extends java.lang.SecurityException {
	/**
	 * Constructs a TRSecurityException with no detail message.
	 * A detail message is a String that describes this particular exception.
	 */
	public TRSecurityException(String name) {
		super(System.getProperty("security." + name, "security." + name));
		System.out.println("*** Security Exception: " + name + " ***");
		printStackTrace();
	}
	
	/**
	 * Constructs a TRSecurityException with the specified detail message.
	 * A detail message is a String that describes this particular exception.
	 * @param s the detail message
	 */
	public TRSecurityException(String name, String arg) {
		super(System.getProperty("security." + name, "security." + name) +
			  ": " + arg);
		System.out.println("*** Security Exception: " + name +
						   ":" + arg + " ***");
		printStackTrace();
	}
}
