package gloop;

import java.util.Dictionary;
import java.util.Enumeration;
import java.util.Hashtable;

public class Naming {

	private Hashtable naming = new Hashtable();
	public static Naming default_naming = new Naming();
	
	public Naming() {
	}
	
	public Naming(Dictionary d) {
		Enumeration k = naming.keys();
		Enumeration v = naming.elements();
		while(k.hasMoreElements()) {
			String s = (String) k.nextElement();
			Object o = v.nextElement();
			bind(s,o);
		}
	}
	
	public Bolg bound(String name) {
		return (Bolg) naming.get(naming.get(name));
	}
	public void bind(String name, Object obj) {
		naming.put(name,new BolgObject(obj));
	}
}
