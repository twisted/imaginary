package divunal.magic;

import twisted.reality.*;

/**
 * For those of you who just *won't* let go of the 'cast frotz on
 * blah' syntax, this is a sort of macro-verb for Spell.
 */

public class Cast extends Verb
{
	public Cast()
	{
		super("cast");
	}
	public boolean action(Sentence d) throws RPException
	{
		Player caster = d.subject();
		String spell = d.directString();
		String cmd;
		if (d.hasIndirect("on"))
		{
			cmd=(spell + " " + d.indirectString("on"));
		}
		else
		{
			cmd=spell;
		}
		caster.hears("(You could just type \""+cmd+"\".)");
		caster.execute(cmd);
		return true;
	}
}
