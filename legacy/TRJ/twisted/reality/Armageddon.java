package twisted.reality;

/**
 * A utility god-verb for halting the universe.  Normally, this is
 * done by a SysV initscript (at least on Linux -- other OS's probably
 * need this more)
 */


class Armageddon extends Verb
{
	public Armageddon()
	{
		super("armageddon");
	}
	public boolean action(Sentence d) throws RPException
	{
		if(d.subject().isGod())
		{
			Age.log("... and then there were none.");
			Age.log("The universe was halted by: " + d.subject().name());
			
			Age.theUniverse().haltTheUniverse();
			
			return true;
		}
		return false;
	}
}
