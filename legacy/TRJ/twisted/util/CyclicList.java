package twisted.util;

public abstract class CyclicList
{
	public final CyclicList nxt()
	{
		return nextLink;
	}
	
	public final CyclicList prv()
	{
		return prevLink;
	}
	
	public final void ignoreN()
	{
		if(nextLink!=null)
			nextLink = nextLink.nxt();
	}
	
	public final void ignoreP()
	{
		if(prevLink != null)
			prevLink = prevLink.prv();
	}
	
	public final void unlink()
	{
		if(prevLink != null)
			prevLink.ignoreN();
		if(nextLink != null)
			nextLink.ignoreP();
	}
	
	public final void linkIn(CyclicList x)
	{
		x.unlink();
		x.setP(this);
		x.setN(nextLink);
		if(nextLink!=null)
			nextLink.setP(x);
		setN(x);
	}
	
	public final void setN(CyclicList x)
	{
		nextLink = x;
	}
	
	public final void setP(CyclicList x)
	{
		prevLink = x;
	}
	
	CyclicList nextLink;
	CyclicList prevLink;
}
