package twisted.reality;

import java.io.IOException;
import java.io.StreamTokenizer;

import twisted.util.SetupWrapper;

import java.util.Vector;

/**
 * This class produces instances of twisted.reality.Thing objects both
 * when the map is parsed (upon startup) and optionally, ingame, from
 * arbitrary input sources.	 For an example of this you can look at
 * twisted.reality.author.Sketch.
 * 
 * @see twisted.reality.author.Sketch
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */
class ThingFactory
{
	public static final int TT_STRING = 34;
	public static final int TT_COMMA = 44;
	public static final int TT_OPENBRACE = 123;
	public static final int TT_CLOSEBRACE = 125;
	public static final int TT_WORD = -3;
	public static final int TT_NUMBER = StreamTokenizer.TT_NUMBER;
	public static final int TT_EOF = -1;
	public static final int TT_EOL = '\n';
	
	
	ThingFactory(StreamTokenizer st,SetupWrapper rsw)
	{
		zq=st;
		sw=rsw;
	}
	
	final Object parsePersistable() throws RPException, IOException
	{
		Object theret;
		if(zq.sval.equals("Name"))
		{
			boolean caps;
			zq.nextToken();
			// ofOf
			caps=Character.isUpperCase(zq.sval.charAt(0));
			zq.nextToken();
			// (
			zq.nextToken();
			// "name"
			ThingIdentifier ti = Age.theUniverse().findIdentifier(zq.sval);
			ThingIdentifier own = null;
			zq.nextToken();
			// ) || ,
			if (zq.ttype == TT_COMMA)
			{
				zq.nextToken();
				// owner
				own = Age.theUniverse().findIdentifier(zq.sval);
				zq.nextToken();
				// )!
			}
			theret = new Name(ti,own,caps);
		}
		else if (zq.sval.equals("Pronoun"))
		{
			ThingIdentifier pronounfor;
			int caps,stat;
			zq.nextToken();
			caps=(Character.isUpperCase(zq.sval.charAt(0)))?1:0;
			if (zq.sval.toLowerCase().equals("of"))
			{
				stat=Pronoun.heshe;
			}
			else if (zq.sval.toLowerCase().equals("obj"))
			{
				stat=Pronoun.himher;
			}
			else
			{
				stat=Pronoun.hisher;
			}
			int finstat = stat|caps;
			zq.nextToken(); // (
			zq.nextToken(); // thing
			pronounfor = Age.theUniverse().findIdentifier(zq.sval);
			zq.nextToken(); // )
			theret = new Pronoun (pronounfor,finstat);
		}
		else
		{
			throw new ExpectedException ("Pronoun or Noun");
		}
		return theret;
	}
	
	final Object parseVectorOrString() throws RPException, IOException
	{
		int zqnt = zq.nextToken();
		if (zqnt==TT_OPENBRACE)
		{
			Vector mvect = new Vector();
			while ((zq.nextToken() != TT_CLOSEBRACE) && (zq.ttype != -1))
			{
				// Age.log(zq);
				switch (zq.ttype)
				{
				case TT_STRING:
					mvect.addElement(zq.sval);
					break;
				case TT_WORD:
					mvect.addElement(parsePersistable());
					break;
				default:
					Age.log("Strange TokenType in parseVectorOrString()");
				case TT_COMMA:
					// The Name that can be named is not the true Name.
					// The Way that can be followed is not the true Way.
					break;
				}
			}
			Object[] x = new Object[mvect.size()];
			mvect.copyInto(x);
			return x;
		}
		else if (zqnt == TT_STRING)
		{
			return zq.sval;
		}
		else
		{
			throw new ExpectedException("{ or a String: but found: "+zq.ttype);
		}
	}
	
	public final void generate() throws RPException, IOException
	{
		int nt;
		nt=zq.nextToken();
		thi = getCurrentThing();
		
		if(nt != TT_OPENBRACE) throw new ExpectedException("{");
		
		while((nt=zq.nextToken())==TT_WORD)
		{
			if(!handleIt(zq.sval.intern()))
				throw new BadWordException(zq.sval);
		}
		
		if(nt != TT_CLOSEBRACE)
			throw new ExpectedException("}");
	}
	
	boolean handleIt(String tok) throws RPException, IOException
	{
		if(tok == "name")
		{
			if(zq.nextToken()==TT_STRING)
			{
				thi.name(zq.sval);
				Age.log("Name: " + zq.sval,Age.VERBOSE);
				return true;
			}
		}
		else if(tok == "describe")
		{
			if(zq.nextToken()==TT_STRING)
			{
				thi.describe(zq.sval);
				Age.log("Description: " + zq.sval,Age.EXTREMELY_VERBOSE);
				return true;
			}
		}
		else if(tok == "place")
		{
			if(zq.nextToken()==TT_STRING)
			{
				sw.addSetup(new PlacementSetup(zq.sval,thi));
				return true;
			}
		}
		else if (tok == "mood")
		{
			if(zq.nextToken()==TT_STRING || zq.nextToken()==TT_WORD)
			{
				Age.log("Mood: " + zq.sval,Age.EXTREMELY_VERBOSE);
				thi.mood(zq.sval);
				return true;
			}
		}
		else if (tok == "feature")
		{
			if(zq.nextToken()==TT_STRING)
			{
				Age.log("Feature: " + zq.sval + "",Age.VERBOSE);
				try {
					thi.addVerb(zq.sval);
				} catch (Exception e) {
					Age.log("Error loading verb on " + thi.NAME() + ": " + e);
				}

				return true;
			}
		}
		else if (tok == "syn")
		{
			if(zq.nextToken()==TT_STRING)
			{
				thi.addSyn(zq.sval);
				Age.log("Synonym: " + zq.sval,Age.EXTREMELY_VERBOSE);
				return true;
			}
		}
		else if (tok == "boolean")
		{
			zq.nextToken();
			String str = zq.sval;
			if(zq.nextToken()==TT_WORD)
			{
				Age.log("[boolean]: " + str + "=" + zq.sval,Age.VERY_VERBOSE);
				
				thi.putBool(str,Boolean.valueOf(zq.sval).booleanValue());
				return true;
			}
		}
		else if (tok == "long")
		{
			zq.nextToken();
			String str = zq.sval;
			if(zq.nextToken()==TT_NUMBER)
			{
				thi.putLong(str,(long) zq.nval);
				Age.log("[long]: " + str + "=" +  zq.nval,Age.VERY_VERBOSE);
				
			}
			return true;
		}
		else if (tok == "float")
		{
			zq.nextToken();
			String str = zq.sval;
			
			if(zq.nextToken()==TT_STRING)
			{
				float num;
				num = Float.valueOf(zq.sval).floatValue();
				thi.putFloat(str, num);
				
				Age.log("[float]: " + str + "=" + num,Age.VERY_VERBOSE);
			}
			else
			{
				Age.log("[float]: " + str + " ???=??? " + zq.sval,Age.VERY_VERBOSE);
			}
			return true;
		}
		else if (tok == "int")
		{
			zq.nextToken();
			String str = zq.sval;
			
			if(zq.nextToken()==TT_NUMBER)
			{
				thi.putInt(str,(int) zq.nval);
				
				Age.log("[int]: " + str + "=" +	 zq.nval,Age.VERY_VERBOSE);
				
			}
			return true;
		}
		else if (tok == "string")
		{
			zq.nextToken();
			String str = zq.sval;
			//if(zq.nextToken() == TT_STRING)
			//{
			// pop goes the paradigm
			thi.putProp(str,parseVectorOrString());
			//Age.log("[string]: " + str + "=" +	zq.sval,Age.VERY_VERBOSE);
			return true;
			//}
		}
		else if (tok == "property")
		{
			zq.nextToken();
			String str = zq.sval;
			if(zq.nextToken() == TT_STRING)
			{
				try
				{
					thi.putDynProp(str,zq.sval);
				} catch (Exception e) {
					Age.log("Error adding dynmaic property to "+thi.name()+": "+e);
				}
				Age.log("[dynamic]: " + str + "=" +	 zq.sval,Age.VERY_VERBOSE);
				return true;
			}
		}
		
		else if (tok == "thing")
		{
			zq.nextToken();
			String str = zq.sval;
			if(zq.nextToken() == TT_STRING)
			{
				Age.log("[thing]: " + str + "=" +  zq.sval,Age.VERY_VERBOSE);
				sw.addSetup( new ThingPropSetup(thi,str,zq.sval) );
				return true;
			}
		}/*
		   else if (tok == "image")
		   {
		   zq.nextToken();
		   thi.setImage(zq.sval);
		   
		   Age.log("Image: " +	zq.sval,Age.EXTREMELY_VERBOSE);
		   
		   return true;
		   }*/
		else if (tok == "handler")
		{
			zq.nextToken();
			String eventname = zq.sval;
			if(zq.nextToken()==TT_STRING)
			{
				Age.log("handles " + eventname + " with " + zq.sval,Age.VERY_VERBOSE);
				try
				{
					thi.putHandler( eventname , zq.sval);
				} catch (Exception e) {
					Age.log("Eorror adding RealEvent handler to "+thi.name()+": "+e);
				}
				return true;
			}
		}
		else if (tok == "descript")
		{
			zq.nextToken();
			String descriptname = zq.sval;
			//if(zq.nextToken()==TT_STRING)
			//{
			//Age.log("Description component: \"" + zq.sval + "\" for " + descriptname, Age.EXTREMELY_VERBOSE );
			// ain't gonna work no more no more
			thi.putDescriptor( descriptname , parseVectorOrString());
			
			return true;
			//}
		}
		else if (tok == "extends")
		{
			if(zq.nextToken()==TT_STRING)
			{
				sw.addSetup ( new SuperSetup(zq.sval,thi) ) ;
				return true;
			}
		}
		else if (tok == "component")
		{
			thi.setComponent(true);
			Age.log("Component bit set",Age.EXTREMELY_VERBOSE);
			return true;
		}
		else if (tok == "theme")
		{
			zq.nextToken();
			thi.theme=zq.sval;
			Age.log("Theme: " + zq.sval,Age.EXTREMELY_VERBOSE);
			return true;
		}
		
		else if (tok == "gender")
		{
			if(zq.nextToken()==TT_WORD)
			{
				thi.setGender(zq.sval.charAt(0));
				Age.log("Gender: "+zq.sval,Age.EXTREMELY_VERBOSE);
				return true;
			}
		}
		else if (tok == "persistable")
		{
			java.util.Dictionary PERSISTS = Age.theUniverse().PERSISTS;
			if (zq.nextToken()==TT_STRING)
			{
				String pname = zq.sval;
				if(zq.nextToken()==TT_STRING)
				{
					String cname = zq.sval;
					/*Age.log("CNAME: "+cname);*/
					/* this should be slightly more paranoid */
					zq.nextToken();
					
					if(zq.sval.equals("key"))
					{
						zq.nextToken();
						thi.putPersistable(pname,
										   (Persistable)
										   PERSISTS.get(zq.sval));
					}
					else
					{
						/* could have a sanity check for "val" here,
						   but it's not too important */
						/*Age.log("val: " + zq.sval);*/
						try {
							Persistable pers = (Persistable) Age.theUniverse().loadClass(cname);
							
							zq.nextToken();
							/*Age.log("content: " + zq.sval);*/
							try
							{
								pers.fromString(zq.sval);
								thi.putPersistable
									(pname,pers);
							}
							catch(Throwable throwable)
							{
								Age.log("Oh no, something has gone HORRIBLY WRONG!!");
								Age.log("(Persistable bug.)");
							}
							
							/* and here's the data */
							zq.nextToken();
							/* could have sanity check for "key" here, but
							   it's not too important*/
							zq.nextToken();
							PERSISTS.put(zq.sval,pers);
						} catch (Exception e) {
							Age.log("Error loading persistable on " + thi.NAME() + ": " + e);
						}
					}
				}
				return true;
			}
		}
		
		return false;
	}
	
	public Thing getCurrentThing()
	{
		if(thi==null) return generatedClass(); else return thi;
	}
	
	public Thing generatedClass()
	{
		return new Thing();
	}
	
	Thing thi;
	SetupWrapper sw;
	StreamTokenizer zq;
}
