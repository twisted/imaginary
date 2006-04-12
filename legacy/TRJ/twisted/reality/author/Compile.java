package twisted.reality.author;	 
import twisted.reality.*;  
import java.io.*; 

/**	 
 * Compile a Java sourcefile so it will be available to the server.
 * Errors will be printed on the log, not to your console, sorry.
 * 
 * This verb relies on quite a few UNIX-isms.  It makes no pretense of
 * being 100% pure Java or in any way cross-platform.
 *	
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */	 

public class Compile extends Verb
{
	public Compile()
	{
		super("compile");
		setDefaultPrep("with");
		sourcepath="trcvs/source";
		// javac="/opt/java/bin/javac";
		javac="/usr/bin/jikes";
	}
	private static String sourcepath;
	private static String javac;
	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;
		String fqpn = d.directString();
		fqpn = fqpn.replace('.','/');
		fqpn = fqpn + ".java";
		
		String[] execr=
		{
			javac,
			"+E",
			"+P",
			"-classpath",
			sourcepath+":/usr/java/lib/classes.zip:.",
			"-d",
			".",
			sourcepath+'/'+fqpn
		};
		d.subject().hears("Compiling " + d.directString() + " ...");

		try
		{
			Process p = Runtime.getRuntime().exec(execr);
			byte byt[] = new byte[5000];
			int retcode;
			retcode=p.waitFor();
			p.getInputStream().read(byt);
			d.subject().hears((new String(byt)).trim());
			p.getErrorStream().read(byt);
			d.subject().hears((new String(byt)).trim());
			
			if(retcode==0)
			{
				d.subject().hears("Done.");
			}
			else
			{
				d.subject().hears("Exited with error code: "+retcode+".	 Check the server log for specific errors.");
			}
		}
		catch (Exception e)
		{
			d.subject().hears("Problem running javac process: "+e);
		}
		return true;
	}
}
