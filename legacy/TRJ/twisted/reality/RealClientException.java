package twisted.reality;

/**
 * This exception indicates that the function called is not supported
 * in this implementation
 *
 * @version 1.0.0, 12 Jun 1999
 * @author James Knight
 */

public class RealClientException extends RuntimeException
{
	public RealClientException(){super();}
	public RealClientException(String s){super(s);}
}
