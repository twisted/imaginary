package demo;

import twisted.reality.*;

public class DemoNamerType extends Verb
{
	public DemoNamerType()
	{
		super("type");
		alias("enter");
		alias("press");
		alias("push");
		setDefaultPrep("on");
	}
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Room room = (Room)d.place();
		Thing thePad = d.verbObject();
		String typed = d.directString();
		String newName = thePad.getString("new name");

		if (typed.startsWith("execute"))
		{
			if (newName.equals(p.name()))
			{
				Object[] pDoesnt = {"You press the \"execute\" key, but nothing interesting happens."};
				Object[] oDoesnt = {p, " pushes a button on the keyboard, and nothing happens."};
				room.tellAll(p, pDoesnt, oDoesnt);
			}
			else
			{
				Object[] pSees = {"You press the \"execute\" key, and there is a blinding flash of light... when your vision clears, you see that your name has changed to ",newName,"."};
				Object[] oSees = {p, " pushes a button on the keyboard, and there is a blinding flash of light as he transforms into ",newName,"."};
				room.tellAll(p, pSees, oSees);
				p.name(newName);
				p.addSyn("dumbname");
			}
		}
		else
		{
			Object[] oTypes = {p, " types something on the keyboard."};
			Object[] pTypes = {"You type \"", typed, "\" on the keyboard."};
		
			thePad.putString("new name", typed);
			thePad.putDescriptor("screen","The screen is black, except for \""+typed+"\" in large green letters.");
			room.tellAll(p, pTypes, oTypes);
		}

		return true;
	}
}
