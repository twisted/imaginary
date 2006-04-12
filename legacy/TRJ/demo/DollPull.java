package demo;

import twisted.reality.*;

public class DollPull extends Verb
{
	public DollPull()
	{
		super("pull");
		alias("squeeze");
		alias("tickle");
		alias("poke");
	}
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Room room = (Room)d.place();
		Thing theDoll = d.directObject();
		String v = d.verbString();

		final String[] dollSpeech = 
		{
			"Design is law!",
			"Daikatana is the best game ever!",
			"Who's a man and a half? I'm a man and a half! A man and a half with a Berserk!",
			"Despite the awful might of the Elder World, you have achieved the Rune of Elder Magic, capstone of all types of arcane wisdom. Beyond good and evil, beyond life and death, the Rune pulsates, heavy with import.",
			"Release dates are nothing but callow lies to decieve the masses.",
			"I work at Ion Storm!",
			"My penthouse office and movie theater has more palm trees than yours.",
			"Design is law!",
			"I'll publish a game any day now, I swear to god!",
			"Gotta love me!",
			"Remember Quake? That was me!!",
			"Invest in Ion Storm! Our creative community is free to focus its energies on building the most compelling games the world has ever seen!",
			"Can I have some more money?",
			"You must have the Flash 3 plugin and Microsoft Internet Explorer (4.0 or greater) to play with me.",
			"DirectX Loves You!",
			"It's never too soon to start paying me for Daikatana!",
			"Poke my belly, and I will design some of the most compelling games ever made!",
			"Design is Law!",
			"Daikatana makes this game look like ass. Ass, I tell you!"
		};

		if (v.equals("pull"))
		{
			Object[] pPull = {"You pull ",theDoll,"'s string."};
			Object[] oPull = {p," pulls ",theDoll,"'s string."};
			Score.increase(p,"john",16);
			room.tellAll(p, pPull, oPull);

			float f = randomf();

			if (f < 0.3)
			{
				Object[] sayA = {twisted.reality.Name.Of(theDoll),"'s string reels back in, and it chirps \"",random(dollSpeech),"\" in a faint, distorted voice."};
				room.tellAll(sayA);
			}
			else if (f < 0.7)
			{
				Object[] sayB = {twisted.reality.Name.Of(theDoll),"'s string reels itself in, and it says, \"",random(dollSpeech),"\" in a faint, high pitched voice."};
				room.tellAll(sayB);
			}
			else
			{
				Object[] sayB = {"As ",twisted.reality.Name.Of(theDoll),"'s string reels in, it squeaks, \"",random(dollSpeech),"\""};
				room.tellAll(sayB);
			}
			return true;
		}
		else
		{
			Object[] pSqueeze = {"You squeeze ",theDoll,"."};
			Object[] oSqueeze = {p," squeezes ",theDoll,"."};
			
			room.tellAll(p, pSqueeze, oSqueeze);
			Object[] squeeze = {twisted.reality.Name.Of(theDoll)," squeaks, \"That tickles!\""};
			room.tellAll(squeeze);
			return true;
		}
	}
}
