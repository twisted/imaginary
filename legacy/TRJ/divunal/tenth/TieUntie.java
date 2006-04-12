package divunal.tenth;

import twisted.reality.*;
import twisted.reality.plugin.clothes.WearRemove;

public class TieUntie extends Verb
{
	public TieUntie()
	{
		super("tie");
		alias("untie");
		alias("do");
		alias("undo");

	}

	public static void tie (Thing cravat)
	{
		String descriptor = cravat.getString("tied descriptor");
		String appearance = cravat.getString("tied appearance");
		cravat.putBool("tied", true);
		cravat.putDescriptor("tie descriptor", descriptor);
		cravat.putString("clothing appearance", appearance);
		Location cravatPlace=cravat.place();
		WearRemove.descript(cravatPlace);
	}

	public static void untie (Thing cravat)
	{
		String descriptor = cravat.getString("untied descriptor");
		String appearance = cravat.getString("untied appearance");
		cravat.putBool("tied", false);
		cravat.putDescriptor("tie descriptor", descriptor);
		cravat.putString("clothing appearance",appearance);
		Location cravatPlace=cravat.place();
		WearRemove.descript(cravatPlace);
	}

    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		Room room = (Room) d.place();
		Thing cravat = d.directObject();
		String v = d.verbString();
		boolean tied = cravat.getBool("tied");
		Object[] oNoTie = 
		{p, " fumbles with ",Name.of(cravat,p)," for a moment."};

		if (v.equals("tie") || v.equals("do"))
		{
			if (tied == false)
			{
				if (cravat.getBool("clothing worn") == true)
				{
					Object[] oTies = 
				{p, " ties ",Name.of(cravat,p),"."};
					Object[] pTies = 
					{"You tie ",cravat,"."};
					tie(cravat);
					room.tellAll(p, pTies, oTies);
				}
				else
				{
					Object[] pDumbAss = {"You should probably wear it before you tie it, or you won't be able to put it on."};
					room.tellAll(p, pDumbAss, oNoTie); 
				}
			}
			else
			{
				Object[] pNoTies = 
				{cravat," is already tied..."};
				room.tellAll(p, pNoTies, oNoTie);
			}
		}
		else
		{
			if (tied == true)
			{
				Object[] oUnTies = 
				{p, " unties ",Name.of(cravat,p),"."};
				Object[] pUnTies = 
				{"You untie ",cravat,"."};
				untie(cravat);
				room.tellAll(p, pUnTies, oUnTies);
			}
			else
			{
				Object[] pNoUnTies = 
				{cravat," isn't tied..."};
				room.tellAll(p, pNoUnTies, oNoTie);
			}
		}
		return true;
	}
}
