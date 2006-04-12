package twisted.reality;
import twisted.util.UnixCrypt;

/**
 * Another restricted-access God verb.  This changes a user's password
 * to a new one with the syntax "passwd user to (unencrypted
 * password)".  Obviously, don't type passwords when other people are
 * standing around your monitor...
 */

class Passwd extends Verb
{
	public Passwd()
	{
		super("passwd");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		((Player)d.directObject()).password=UnixCrypt.crypt(d.indirectString("to"),d.directObject().NAME());
		return true;
	}
}
