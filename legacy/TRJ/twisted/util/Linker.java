package twisted.util;

final class Linker
{
	Linker(Linker n,Object o)
	{
		next=n;
		val=o;
		key=val;
		if(key!=null) hash=key.hashCode();
	}
	
	Linker(Linker n, Object k, Object v)
	{
		next=n;
		val=v;
		key=k;
		if(k!=null) hash=k.hashCode();
	}
	
	Linker next;
	public Object val;
	public Object key;
	public int hash;
}
