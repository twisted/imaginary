package twisted.reality.author; 
import twisted.reality.*; 
import java.io.*;

/** 
 * Do CVS stuff.  Usage is to do a "cvs FQCN" and it'll open the file
 * for editing. (where FQCN is a Fully Qualified java Class Name)
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */ 

public class CVS extends Verb 
{ 
	private static String CVSROOT;
	private static String cvsplace;
	class CVSproc implements ResponseProcessor
	{
		String file;
		String root;
		String verb;
		Player player;
		String cvsdir;
		
		CVSproc(String toEdit,
				String toRoot,
				String originalVerb,
				Player toInteract,
				String place)
		{
			root=toRoot;
			verb=originalVerb;
			player=toInteract;
			cvsdir=place;
			file=cvsdir+'/'+toEdit;
		}
		
		public void gotResponse(String response)
		{
			if (response.equals(verb))
			{
				player.hears("You didn't change anything.");
			}
			else
			{
				try
				{
					player.hears("Writing file...");
					FileWriter fwr=new FileWriter(file);
					fwr.write(response);
					fwr.flush();
					fwr.close();
					player.hears("Done.");
				}
				catch(IOException ioe)
				{
					player.hears("Whoops.  CVS file error.");
					return;
				}
				String[] execr =
				{
					"cvs",
					"-d",
					root,
					"-q",
					"commit",
					"-m",
					"TR/CVS 0.1 COMMIT MESSAGE. "+player.NAME()+" IS RESPONSIBLE.",
					file				
				};
				try
				{
					player.hears("Executing update...");
					Process p = Runtime.getRuntime().exec(execr);
					p.waitFor();
					player.hears("Done.");
				}
				catch(Exception ioe)
				{
					player.hears("Couldn't exec.");
				}
			}
		}
	}
	
	public CVS() 
	{ 
		super("cvs");
		setDefaultPrep("with");
		/*
		 * We don't need a "login" phase because the game server is
		 * really the same as the cvs server.  May need it in the future...
		 * 
		 * This verb will *NOT* work anywhere but divunal right now,
		 * mostly because of this.
		 * 
		 * Actually, scratch that.	This will work anywhere that uses the same CVS structure, it's fairly simple to follow... and we don't actually use the word Divunal anywhere, either, it's just "TR"cvs and "reality/cvs".
		 */
		CVSROOT="/home/cvs";
		cvsplace="trcvs/source";
	} 
	
	public boolean action(Sentence d) throws RPException 
	{
		if(!d.subject().isGod())
		{
			d.subject().hears("Umm... no.");
			return true;
		}
		String fqpn = d.directString();

		fqpn = fqpn.replace('.','/');
		fqpn = fqpn + ".java";
		
		File myf = new File(cvsplace+'/'+fqpn);
		char[] tmpbyte=new char[(int)myf.length()];
		d.subject().hears("Attempting to update the CVS tree...");
		String[] execr =  
		{ 
			"cvs",
			"-d",
			CVSROOT,
			"-q",
			"update",
			"-d",
			cvsplace
		}; 
		
		try
		{
			Process p = Runtime.getRuntime().exec (execr);
			p.waitFor();
		}
		catch (Exception ioe)
		{
			d.subject().hears("Couldn't exec.");
		}
		d.subject().hears("Done.");
		try
		{
			FileReader fre = new FileReader(myf);
			fre.read(tmpbyte);
			fre.close();
		}
		catch (IOException ioe)
		{
			d.subject().hears("Not editing any file.");
			return true;
		}
		String fullyRead=(new String(tmpbyte)).trim();
		d.subject().requestResponse(new 
									CVSproc(fqpn,
											CVSROOT,
											fullyRead,
											d.subject(),
											cvsplace),
									"TR/CVS: " + fqpn,
									fullyRead);
		
		return true;
	} 
}
