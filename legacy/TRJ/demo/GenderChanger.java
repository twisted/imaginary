package demo;

import twisted.reality.*;

public class GenderChanger extends Verb
{
	public GenderChanger()
	{
		super("push");
		alias("press");
	}
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Room room = (Room)d.place();
		Thing theChanger = d.verbObject();
		String typed = d.directString();
		char g = theChanger.getGenderTo(p);
		char pg = p.getGenderTo(p);

		if (g == pg)
		{
			Object[] pDoesnt = {"You press the button, but nothing interesting happens."};
			Object[] oDoesnt = {p, " pushes a button on the gender changer, but nothing happens."};
			room.tellAll(p, pDoesnt, oDoesnt);
		}
		else
		{
			String genderText, genderDesc, genderPronoun;

			if (g == 'm')
			{
				genderText = "more masculine.";
				genderDesc = "masculinity.";
				genderPronoun = "fellow";
			}
			else if (g == 'f')
			{
				genderText = "more feminine.";
				genderDesc = "femininity.";
				genderPronoun = "woman";
			}
			else
			{
				genderText = "less sexual.";
				genderDesc = "gender neutrality.";
				genderPronoun = "person";
			}

			Object[] pSees = {"You press the button, and there is a blinding flash of light... when your vision clears, you feel a great deal ",genderText};
			Object[] oSees = {p, " pushes a button on the keyboard, and there is a blinding flash of ",genderDesc};

			room.tellAll(p, pSees, oSees);
			p.setGender(g);
			p.putString("gender pronoun", genderPronoun);
			p.setFocus(p);
		}
			if (g == 'm')
			{
				g = 'f';
			}
			else if (g == 'f')
			{
				g = 'n';
			}
			else 
			{
				g = 'm';
			}

			theChanger.setGender(g);

		return true;
	}
}
