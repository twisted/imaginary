package divunal.common;

import twisted.reality.*;
import java.util.*;

public class Study extends Verb
{
	public Study()
	{
		super("study");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		Thing book = d.directObject();
		String subject = book.getString("subject skill");
		Player reader = d.subject();
		
		float f = reader.getFloat(subject+" skill");
		
		if (f <= book.getFloat("base"))
		{
			reader.putFloat(subject+" skill",book.getFloat("base"));
			reader.putBool(subject+" ability",true);
			reader.putLong(subject+" train",System.currentTimeMillis());
		}
		else
		{
			reader.hears("You already know how to do that.  You might want to practice it...");
		}
		Object[] rdr={reader," flips through ",book,", studying intently."};
		//d.place().tellEverybodyBut(reader,reader.name() + " flips through " + book.the() + book.name() + ", studying intently.");
		d.place().tellAll(reader,null,rdr);
		return true;
	}
}
