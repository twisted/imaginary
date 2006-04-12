package gloop;

import java.lang.reflect.*;
import java.util.Hashtable;
import java.util.Vector;

public class BolgObject implements Bolg
{
	private Hashtable methods=new Hashtable();
	Object wrapped;
	
	private void addMethod(String name, Method m) {
		Object z = methods.get(name);
		if (z!=null) {
			if (z instanceof Vector) {
				((Vector)z).addElement(m);
			} else {
				Vector v = new Vector();
				v.addElement(z);
				v.addElement(m);
				methods.put(name,v);
			}
		}
		else
			methods.put(name,m);
	}
	
	public BolgObject(Object toWrap) {
		Class c = toWrap.getClass();
		Method[] crystal = c.getMethods();
		for (int ball = 0; ball < crystal.length; ball++) {
			Method man = crystal[ball];
			addMethod(man.getName(),man);
		}
	}
	
	public void set(String key, Object value) throws NoSuchFieldException {
		try {
			wrapped
				.getClass()
				.getField(key)
				.set(wrapped,value);
		} catch(IllegalAccessException iae) {
			throw new NoSuchFieldException(key);
		}
	}
	
	public Object get(String key)
		throws NoSuchFieldException {
		try {
			return wrapped
				.getClass()
				.getField(key)
				.get(wrapped);
		} catch(Exception nsfe) {
			Object q = methods.get(key);
			if (q!=null)
				return new BolgMethod(this,q);
			if (nsfe instanceof NoSuchFieldException)
				throw (NoSuchFieldException) nsfe;
			else
				throw new NoSuchFieldException(key);
		}
	}
	public Object call(Object[] args) throws IllegalArgumentException {
		throw new IllegalArgumentException("this object is not callable");
	}
	
	public int hashCode() {
		return wrapped.hashCode();
	}
}
