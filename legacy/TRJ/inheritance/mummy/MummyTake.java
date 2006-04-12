package inheritance.mummy;

import twisted.reality.*;

public class MummyTake extends Verb
{
	public MummyTake()
	{
		super("take");
	}
	
	public boolean action(Sentence d)
	{
		try
		{
			d.subject().putHandler("startup","inheritance.mummy.RotHandler");
			d.subject().handleDelayedEvent ( new RealEvent("startup",null,null),1);
		}
		catch(ClassNotFoundException cnfe)
		{
			/* This should probably print an error message --
			   but to where? */
		}
		return false;
	}
}
