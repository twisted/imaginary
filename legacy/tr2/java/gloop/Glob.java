package gloop;

import java.io.IOException;

public class Glob
{
	Gloop gloop;
	Integer glid;
	public Glob(Gloop gloop, Integer glid)
	{
		this.gloop=gloop;
		this.glid=glid;
	}
	
	public Object get(String key) throws IOException
	{
		return gloop.sendGet(glid,key);
	}
	
	public void set(String key, Object value) throws IOException
	{
		gloop.sendSet(glid,key,value);
	}
	
	public Object call(Object[] args) throws IOException
	{
		return gloop.sendCall(glid,args);
	}
}
