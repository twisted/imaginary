package twisted.reality;

import java.io.*;
import java.net.*;

class RealityServer extends Thread
{
	int i=1;
	int port;
	
	// disallow default constructor
	private RealityServer() { }

	public RealityServer(int p)
	{
		port = p;
	}
	
	public void run()
	{
		Socket incoming=null;
		try
		{
			ServerSocket s = new ServerSocket(port);
			for(;;)
			{
				incoming = s.accept();
				Age.log("Incoming " + incoming.getInetAddress().getHostAddress() + " on Reality:" + i + ".");
				new NetClientUser(incoming,i);
				i++;
			}
		}
		catch(Exception e)
		{
			try
			{
				incoming.close();
			}
			catch(Exception eeee) {}
			Age.log(e);
			Age.log("Reality Server failure.");
		}
	}
}
