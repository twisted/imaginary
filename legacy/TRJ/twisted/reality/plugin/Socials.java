/**
 * Reads a list of socials from a file, allowing you to make lots of
 * similarly structured Social verbs without needing separate verb
 * classes. See comments for format.
 *
 * @version 1.0.0, Aug 7 1999
 * @author James Knight */

package twisted.reality.plugin;

import twisted.reality.*;
import java.util.Hashtable;
import java.util.Vector;
import java.util.Enumeration;

import java.io.*;

/*
Escape codes for use in social strings:
$$ = $ (two dollar signs together makes one in the output)
$[12]n = name of [person/target]
$[12]s = his/her of [person/target]
$[12]m = him/her of [person/target]
$[12]e = he/she of [person/target]

 Example of a socials.txt file...
#bite
hidden false
cnoarg You nervously gnaw at your lower lip.
onoarg $1n gnaws nervously at $s lower lip.
cfound You bite $2n!
vfound $1n bites you!
ofound $1n bites $2n!
notfound You can't bite someone who isn't here.
cself You bite yourself on the arm!
oself $1n bites himself on the arm!
ofoundobj $1n bites $2n savagely.  Run you fool!!  Rabid $1n on the loose!
cfoundobj You foam at the mouth and bite $2n, with a crazed and rabid look in your eyes.

#smile
<etc...>

<more socials.....>

#END
 */
public class Socials extends Verb
{
	final class SocialType
	{
		String name;
		boolean hidden; // this is meant to be whether it is not shown if the reciever
						// can't see the person doing it. Things like yell would not be hidden
						// things like smile would be hidden.
		String position; // ?? positions you can do this social from or something...
		
		String cnoarg;
		String onoarg;
		String cfound;
		String ofound;
		String vfound;
		String cfoundobj;
		String ofoundobj;
		String notfound;
		String cself;
		String oself;
	}
	Hashtable socials;
	
	String readLine(BufferedReader r) throws IOException
	{
		String s;
		while ((s = r.readLine()).equals("")) ;
		return s;
	}
	
	public Socials()
	{
		super("socials");
		File file = new File("socials.txt");
		socials = new Hashtable();
		try
		{
			InputStream fs = new FileInputStream(file);
			LineNumberReader r = new LineNumberReader(new InputStreamReader(fs, "UTF8"));

			SocialType s = null;
			while(true)
			{
				String line = readLine(r);
				if(line.charAt(0) == '#') // new social
				{
					if(s != null)
					{
						socials.put(s.name, s);
						alias(s.name);
					}
					if(line.equals("#END"))
						break;
					s = new SocialType();
					s.name = line.substring(1);
					continue;
				}
				
				int pos = line.indexOf(' ');
				String field = line.substring(0, pos).intern();
				String arg = line.substring(pos + 1);
				
				if(field == "cnoarg")
					s.cnoarg = arg;
				else if(field == "onoarg")
					s.onoarg = arg;
				else if(field == "cfound")
					s.cfound = arg;
				else if(field == "ofound")
					s.ofound = arg;
				else if(field == "vfound")
					s.vfound = arg;
				else if(field == "notfound")
					s.notfound = arg;
				else if(field == "cself")
					s.cself = arg;
				else if(field == "oself")
					s.oself = arg;
				else if(field == "cfoundobj")
					s.cfoundobj = arg;
				else if(field == "ofoundobj")
					s.ofoundobj = arg;
				else if(field == "hidden")
					s.hidden = arg.equals("true");
				else
					Age.log("Socials error parsing file: no such directive as "+arg+".");
			}
		}
		catch (java.io.IOException e)
		{
			Age.log(e);
			Age.log("Couldn't read socials file properly.");
		}
		catch (NumberFormatException e)
		{
			Age.log(e);
		}
		
	}
	
	Object[] parseSocString(String s, Thing p, Thing t)
	{
		Vector v = new Vector();
		int pos = 0;
		if (s == null) return null;
		int len = s.length();
		try
		{
			while(true)
			{
				int oldpos = pos;
				int newpos;
				/* Find $ but not $$ */
				while (true)
				{
					newpos = s.indexOf('$', oldpos);
					if(newpos == -1)
						break;
					if(s.charAt(newpos + 1) == '$')
						oldpos = newpos + 2;
					else break;
				}
				if(newpos == -1)
				{
					v.addElement(s.substring(pos));
					break;
				}
				
				v.addElement(s.substring(pos, newpos));
				char who = s.charAt(newpos + 1);
				char what = s.charAt(newpos + 2);
				if(who != '1' && who != '2')
				{
					Age.log("Invalid social string: \"" + s + "\". Invalid target '"+who+"'.");
					break;
				}
				Thing w = who == '1'?p:t;
				if(what == 'n')
					v.addElement(Name.of(w));
				else if(what == 'e')
					v.addElement(Pronoun.of(w));
				else if(what == 'm')
					v.addElement(Pronoun.obj(w));
				else if(what == 's')
					v.addElement(Name.of("",w));
				pos = newpos + 3;
			}
		} catch (StringIndexOutOfBoundsException e) {
			Age.log("Invalid social string: \"" + s + "\". $ escape without any following characters");
		}
		Object[] o = new Object[v.size()];
		v.copyInto(o);
		return o;
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Thing r = null;
		String rs = null;
		Player p = d.subject();
		String verbString = d.verbString();
		
		if(verbString.equals("socials"))
		{
			Enumeration keys = socials.keys();
			p.hears("Socials:");
			while(keys.hasMoreElements())
			{
				String name = (String) keys.nextElement();
				p.hears("  " + name);
			}
			return true;
		}
		
		SocialType soc = (SocialType)socials.get(d.verbString());
		if(soc == null)
		{
			return false;
		}
		
		if(d.hasDirect())
		{
			rs = d.directString();
			if(d.hasDirectObject())
				r = d.directObject();
		}
		else if (d.hasIndirect("at"))
		{
			rs = d.indirectString("at");
			if(d.hasIndirectObject("at"))
				r = d.indirectObject("at");
		}
		
		if(rs == null)
		{
			d.place().tellAll(p, parseSocString(soc.cnoarg, p, null), parseSocString(soc.onoarg, p, null));
		}
		else if(r == null)
		{
			p.hears(parseSocString(soc.notfound, p, null));
		}
		else if(r == p)
		{
			d.place().tellAll(p, parseSocString(soc.cself, p, r), parseSocString(soc.oself, p, r));
		}
		else
		{
			if(r instanceof Player) // FIXME: BAD BAD CODE...should call Thing.isSentient() which doesn't exist yet.
				d.place().tellAll(p, r, parseSocString(soc.cfound, p, r), parseSocString(soc.vfound, p, r), parseSocString(soc.ofound, p, r));
			else
				d.place().tellAll(p, parseSocString(soc.cfoundobj, p, r), parseSocString(soc.ofoundobj, p, r));				
		}
		return true;
	}
}
