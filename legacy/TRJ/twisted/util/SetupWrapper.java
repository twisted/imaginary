package twisted.util;

public class SetupWrapper extends RecursiveSetup
{
	RecursiveSetup first;
	
	public void addSetup(RecursiveSetup a)
	{
		if(a != null)
		{
			a.next=first;
			first=a;
		}
	}
	
	public void wrapper()
	{
		if(first != null) first.wrapUp();
	}
}
