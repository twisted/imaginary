package twisted.util;

public abstract class RecursiveSetup
{
	RecursiveSetup next;
	
	public void wrapUp()
	{
//		wrapper();
//		if(next != null) next.wrapUp();
// Recursion is slow and buggy in java, so while it will continue to *look* like it's working like that, a faster implementation should be:
		RecursiveSetup r = this;
		while (r!=null)
		{
			r.wrapper();
			r=r.next;
		}
	}
	
	public abstract void wrapper();
}
