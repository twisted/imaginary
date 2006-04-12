package demo;

import twisted.reality.*;

/**
 * This is an authoring verb which repopulates an object in the demo
 * area to its original location.
 * 
 * @author Tenth */

public class Repop extends Verb
{
	public Repop()
	{
		super("repop");
		setDefaultPrep("with");
	}

	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Thing o = d.directObject();
 		Location repop = (Location) o.getThing("repop");

		if (repop == null)
		{
			Object[] doh = {o, " doesn't react."};
			p.hears(doh);
		}
		else if ((o.place() instanceof Player) && (o.place() != p))
		{
			Object[] good = {"Be good, ",p,", Be good!"};
			p.hears(good);
		}
		else
		{
			Object[] pPops = {"You wave ",o," away to where it belongs."};
			Object[] oPops = {p," waves dismissively at ",o,", and it goes back to where it once belonged."};
			Object[] leavearrive={o," repopulates."};
			o.setComponent(false);
			o.moveTo(repop,leavearrive);
			d.place().tellAll(p, pPops, oPops);
		}
		return true;
	}
}
