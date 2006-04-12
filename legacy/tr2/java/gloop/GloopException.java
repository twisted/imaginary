package gloop;

import java.io.StringWriter;
import java.io.PrintWriter;
import java.io.PrintStream;

public class GloopException extends Exception {
	/**
	 * Not too much to say about this...
	 */
	String traceback;
	public GloopException(String s, String tb){
		super(s);
		traceback=tb;
	}

	public GloopException(String s) {
		super(s);
	}

	public GloopException(String s, Throwable t) {
		super(s,_getStackTrace(t));
	}
	
	public void printStackTrace() {
		printStackTrace(System.out);
	}
	
	public void printStackTrace(PrintWriter s) {
		super.printStackTrace(s);
		s.println("* Gloop Remote Trace Follows: \n"+traceback);
	}
	
	public void printStackTrace(PrintStream s) {
		printStackTrace(new PrintWriter(s));
	}
	
	public String getStackTrace() {
		return _getStackTrace(this);
	}
	
	public static String _getStackTrace(Throwable t) {
		StringWriter sw = new StringWriter();
		PrintWriter pw = new PrintWriter(sw);
		t.printStackTrace(pw);
		return sw.toString();
	}
}
