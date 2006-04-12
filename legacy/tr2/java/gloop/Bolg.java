package gloop;

import java.lang.reflect.*;

public interface Bolg
{
	public void set(String key, Object value)
		throws NoSuchFieldException;

	public Object get(String key)
		throws NoSuchFieldException;
	
	public Object call(Object[] args)
		throws IllegalAccessException, InvocationTargetException, IllegalArgumentException;
}
