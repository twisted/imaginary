package twisted.reality;

import java.awt.*;
import java.io.*;
import java.util.*;

/**
 * This is the class which starts the server. It starts all
 * appropriate junk and then sits there waiting for connections. The
 * correct commandline syntax (if you're not using a Mac) is - java
 * twisted.reality.Pump #filename#.	 In the mac version, the map you
 * wish to load must be entitled 'map.por'
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Pump
{
	/**
	 * The "main" method that starts the program.
	 */
	
	public static void main(String args[])
	{
		int port = 8889;
		
		/* log *all* messages to the redirected Age.log file */
		System.setErr(System.out);
		/* can't do this: System.err=System.out;*/
		/* and away we go. */
		System.out.println("Twisted Reality v"+Age.version);
		System.out.println("(c) 1999 Twisted Matrix Enterprises");
		System.out.println("Please wait...");
		for(int i = 1; i < args.length; i++)
		{
			if (args[i].startsWith("-v"))
			{
				Age.verbosity=Integer.parseInt(args[i].substring(2));
				Age.log("Verbosity: " + Age.verbosity);
			}
			else if (args[i].startsWith("-p"))
			{
				port = Integer.parseInt(args[i].substring(2));
			}
		}
		
		if(args.length > 0)
			Age.LoadAge(args[0]);
		else Age.LoadAge(null);
		
		(new RealityServer(port)).start();
		(new PumpKillServer (port + 1)).start();
		Age.log ("Port: " + port);
	}
}
