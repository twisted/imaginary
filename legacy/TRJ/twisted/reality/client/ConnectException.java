package twisted.reality.client;

/**
 * This exception is thrown from Faucet.connectUp to indicate a failure to negotiate
 * the protocol startup, or because of an incorrect user/pass.
 *
 * @version 1.0.0, 8 Jul 1999
 * @author James Knight
 */

public class ConnectException extends Exception
{
	public ConnectException(){super();}
	public ConnectException(String s){super(s);}
	public String toString()
	{
		return getMessage();
	}
}
