package divunal.common.author;

import twisted.reality.*;

public class DarkDescribe extends Verb
{
	public DarkDescribe()
	{
		super("darkdescribe");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Object[] dsc = {"Please enter a dark description for " + d.directObject(),"."};
		d.subject().hears(dsc);
		d.subject().requestResponse(
			 new DarkDescribeProcessor(d.directObject(),d.subject()),"Dark description of "
			 + d.directObject().nameTo(d.subject()) + ".",d.directObject().getString("darkDescription"));
		return true;
	}
}
