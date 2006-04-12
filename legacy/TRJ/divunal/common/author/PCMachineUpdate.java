package divunal.common.author;

import twisted.reality.*;

public class PCMachineUpdate extends RealEventHandler
{
	public void gotEvent(RealEvent r, Thing t)
	{

		Thing str = t.getThing("strength");
		Thing dex = t.getThing("dexterity");
		Thing ndu = t.getThing("endurance");
		Thing mem = t.getThing("memory");
		Thing agl = t.getThing("agility");
		Thing psy = t.getThing("psyche");
		
		float strength = str.getFloat("value");
		float dexterity = dex.getFloat("value");
		float endurance = ndu.getFloat("value");
		float memory = mem.getFloat("value");
		float agility = agl.getFloat("value");
		float psyche = psy.getFloat("value");

		float maxStuff = 0;
		float actStuff = strength+dexterity+endurance+memory+agility+psyche;

		float left = maxStuff-actStuff;

		left -= left % 0.05;
		
		String color;
		if (left < 0)
		{
			color="red";
		}
		else if (left > 0)
		{
			color="yellow";
		}
		else
		{
			color="green";
		}
		String name = t.getString("player name");
		String dials = 
			"Strength is set to "+strength+". "+
			"Agility is set to "+agility+". "+
			"Dexterity is set to "+dexterity+". "+
			"Endurance is set to "+endurance+". "+
			"Psyche is set to "+psyche+". "+
			"Memory is set to "+memory+". "+
			"The black \"Point Total\" rectangle is displaying the number \""+left+
			"\" in a "+color+" script, and the \"Name\" rectangle " +
			((name == null) ? "is blank." : "is displaying: \""+name+"\" in a " + ((Age.theUniverse().findThing(name)==null)?"bright white":"dark grey") +" script.");
		
		
		t.putDescriptor("dials",dials);
		Thing mperson = t.getThing("tube").getThing("person");
		
		/* infuse those attributes! */

		if(mperson != null)
		{
			String title, eyeColor, eyeStyle, hairColor, hairTone, hairStyle, complexion, demeanor, build, face, randomDesc;
			float pran;

			// Apply the stats

			mperson.putFloat("dexterity",dexterity);
			mperson.putFloat("endurance",endurance);
			mperson.putFloat("agility",agility);
			mperson.putFloat("strength",strength);
			mperson.putFloat("memory",memory);
			mperson.putFloat("psyche",psyche);

			// Build the random description

			if (randomf() > 0.5)
			{
				mperson.setGender('m');
				face = random(maleFaces);
				if (randomf() > 0.5)
					title = "young man";
				else
					title = "man";					
			}
			else
			{
				mperson.setGender('f');
				face = random(femaleFaces);
				if (randomf() > 0.5)
					title = "woman";
				else
					title = "young woman";
			}

			if (psyche > randomf()+0.1)
				complexion = random(divuthanComplexions);
			else if (endurance < -0.3)
				complexion = random(sicklyComplexions);
			else
				complexion = random(complexions);

			if (psyche > (randomf()+0.1))
				eyeColor = random(divuthanEyeColors);
			else
				eyeColor = random(eyeColors);

			if (psyche > randomf()+0.2)
				eyeStyle = random(divuthanEyeStyles);
			else
				eyeStyle = random(eyeStyles);

			if (psyche > randomf())
			{
				hairTone = random(divuthanHairTones);
				hairColor = random(divuthanHairColors);
			}
			else
			{
				hairTone = random(hairTones);
				hairColor = random(hairColors);
			}
			hairStyle = random(hairStyles);

			if (memory > randomf()+0.2)
				demeanor = random(memoryDemeanors);
			else
				demeanor = random(demeanors);

			if (strength > 0.3 && endurance > 0.3 && agility > 0.3)
				build = random(perfectBuild);
			else if (strength > 0.3 && endurance > 0.3)
				build = random(strongBuild);
			else if ((agility > 0.3)&&(strength > 0.3 || endurance > 0.3))
				build = random(agileBuild);
			else if (agility > 0.3)
				build = random(thinBuild);
			else if (strength > -0.3 && endurance > -0.3 && agility > -0.3)
				build = random(normalBuild);
			else if (strength > 0.3)
				build = random(fatBuild);
			else build = random(sickBuild);

			pran = randomf();

			if (pran < 0.3)
			{
				randomDesc = "(Test Version: Type A) "
				+Thing.AAn(build)+build+", "+demeanor+" looking "+title
                +" with "+eyeStyle+" "+eyeColor+" eyes, "
				+hairStyle+" "+hairTone+" "+hairColor+" hair, and a "
				+complexion+" complexion.";
			}
			else if (pran < 0.6)
			{
				randomDesc = "(Test Version: Type B) "
				+Thing.AAn(build)+build+" "+title+" with "
				+hairStyle+" "+hairColor+" hair, "+eyeStyle+" "+eyeColor
				+" eyes, and "+Thing.aan(demeanor)+demeanor+", "+face
				+" face.";
			}
			else
			{
				randomDesc = "(Test Version: Type C) "
				+"A "+title+" with ";
				if (randomf() < 0.5)
					randomDesc += hairTone+", ";
				randomDesc += hairStyle+" "+hairColor
				+" hair and "+eyeColor+" eyes. "
				+new Pronoun(mperson,Pronoun.HESHE).toStringTo(mperson)
				+" is "+build+", ";
				if (randomf() < 0.5)
					randomDesc += "with "+complexion+" skin and ";
				else
					randomDesc += "and has ";
				randomDesc += "a "+face+", "+demeanor+" face.";
			}
		

			mperson.describe(randomDesc);
		}
	}
	
	public static final String[] eyeColors =
	{
		"blue", "grey", "green", "brown", "hazel", "yellow", "pink", "purple", "amber"
	};
	
	public static final String[] divuthanEyeColors =
	{
		"red", "violet", "bright white", "silver", "translucent pink"
	};
	
	public static final String[] divuthanEyeStyles =
	{
		"gleaming", "shining", "sunken", "piercing", "bright", "cold"
	};
	
	public static final String[] eyeStyles =
	{
		"bright", "light", "soft", "clear", "wide", "dark", "cold", "cloudy", "stormy", "slanted", "almond-shaped"
	};
	
	public static final String[] hairColors =
	{
		"blonde", "gold", "copper", "brown", "red", "blue", "green", "purple", "pink", "grey", "auburn", "violet"
	};
	
	public static final String[] divuthanHairColors =
	{
		"jet black", "gray", "silver", "white", "sable"
	};
	
	public static final String[] hairTones = 
	{
		"bright", "light"
	};
	
	public static final String[] divuthanHairTones =
	{
		"glossy", "shiny"
	};
	
	public static final String[] hairStyles =
	{
		"unkempt", "messy", "uneven", "stringy", "curly", "wavy", "straight", "neat", "neatly trimmed", "smooth", "sleek", "thin", "sparse", "cropped", "short", "shoulder length", "long", "flowing"
	};
	
	public static final String[] complexions =
	{
		"light", "pale", "freckled", "tanned", "dark"
	};

	public static final String[] sicklyComplexions =
	{
		"extremely pale", "pale", "unhealthy", "sickly"
	};
	
	public static final String[] divuthanComplexions =
	{
		"white", "extremely pale", "translucent", "greyish"
	};
	
	public static final String[] demeanors =
	{
		"solemn", "thoughtful", "mischievous", "wry", "distant", "cold","troubled", "bright", "proud", "nervous", "haughty", "crazy", "mysterious", "inscrutable", "youthful", "tired", "shifty", "lively", "personable", "crafty", "stern", "wise"
	};
	
	public static final String[] maleFaces =
	{

		"crooked", "round", "thin", "narrow", "jagged", "sharply pointed", "bony", "angular", "weathered", "rough", "grizzled", "handsome"
	};

	public static final String[] femaleFaces =
	{
		"round", "thin", "narrow", "sharply pointed", "angular", "smooth", "rosy", "pretty", "beautiful"
	};

	public static final String[] memoryDemeanors =
	{
		"friendly", "gentle", "cheerful", "peaceful", "serene", "calm", "good natured"
	};
	
	public static final String[] perfectBuild=
	{
		"imposing", "statuesque", "finely sculpted", "well proportioned"
	};
	public static final String[] agileBuild=
	{
		"agile", "sinuous", "athletic", "lean", "well poised"
	};
	
	public static final String[] normalBuild=
	{
		"tall", "short", "thin", "lean", "small", "heavy set", "large"
	};
	
	public static final String[] strongBuild=
	{
		"muscular", "hefty", "huge", "broad shouldered", "powerfully built"
	};
	
	public static final String[] thinBuild=
	{
		"thin", "lean", "skinny", "gracefully built"
	};
	
	public static final String[] sickBuild=
	{
		"weak", "scrawny", "gaunt", "frail"
	};
	
	public static final String[] fatBuild=
	{
		"portly", "overweight", "blocky", "large" 
	};
}
