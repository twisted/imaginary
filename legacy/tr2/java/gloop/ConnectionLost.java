package gloop;
import java.io.IOException;

public class ConnectionLost extends GloopException {
	public ConnectionLost(IOException ioe) {
		super("Connection Lost",ioe);
	}
}
