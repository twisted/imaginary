package twisted.reality;

import java.io.*;
import java.net.*;
import twisted.util.UnixCrypt;

class PumpKillServer extends Thread
{
	int i=1;
	int port;

	// disallow default constructor
	private PumpKillServer() { }

	public PumpKillServer(int p)
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

				try
				{
					BufferedReader in  = new BufferedReader(new InputStreamReader(incoming.getInputStream()));
					PrintWriter out = new PrintWriter (new OutputStreamWriter(incoming.getOutputStream()));
					
					String login = in.readLine();
					String password = in.readLine();
					
					Thing foo = Age.theUniverse().findThing(login);
					
					if( (foo != null) && (foo instanceof Player) )
					{
						Player plr = (Player) foo;
						if (plr.password.equals(UnixCrypt.crypt(password,plr.password))&& plr.isGod())
						{
							Age.log("Mr. Book said, \"SHUT IT DOWN!\", and so did " + login);
							Age.theUniverse().haltTheUniverse(false);
							
							out.println("1");
							out.flush();
							out.close();
							System.exit(0);
						}
						else
						{
							Age.log("Attempt to shut down server with a bad password.  Erk!");
							Age.log("User was: " + login);
							out.println("0");
							out.flush();
							out.close();
						}
					
					}
					else
					{
						Age.log("Attempt to shut down server with a bad password.  Erk!");
						Age.log("User was: " + login);
						out.println("0");
						out.flush();
						out.close();
					}
					
				}
				catch(Exception e)
				{
					// forget about it
				}
			}
		}
		catch(Exception e)
		{
			try
			{
				incoming.close();
			}
			catch(Exception eeee) {}
		}
	}
}
