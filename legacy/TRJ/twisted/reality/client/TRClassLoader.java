package twisted.reality.client;

import java.io.InputStream;
import java.util.Hashtable;
import java.net.URL;
import java.net.URLConnection;
/**
 * This class allows for dynamic reloading of verbs in
 * twisted.reality.	 Bits of it are hard-coded right now.  Not to be
 * taken orally.
 */

public class TRClassLoader extends ClassLoader
{
	private String	  urlString;
	private Hashtable classes = new Hashtable();
	
	/**
	 * Make a new TRClassLoader
	 */
	public TRClassLoader(String urlString)
	{
		super();
		if(System.getSecurityManager() != null)
			System.getSecurityManager().checkCreateClassLoader();
		this.urlString = urlString;
	}
	
	/**
	 * Load a class.
	 */
	protected Class loadClass(String name, boolean b) throws ClassNotFoundException
	{
		Class c;
		
		// first, check the cache.
		c = (Class)classes.get(name);
		if (c != null) return c;
		
		// Check with the primordial class loader
		try {
			return findSystemClass(name);
		} catch (ClassNotFoundException e) { }
		
		// okay, not a system class, now try loading it ourselves...
		String className = name.replace('.','/')+".class";
		try {
			URL url = new URL(urlString + className);
			URLConnection connection = url.openConnection();
			
			InputStream inputStream = connection.getInputStream();
			int length = connection.getContentLength();
			
			byte[] data = new byte[length];
			inputStream.read(data); // Actual byte transfer
			inputStream.close();
			c = defineClass(name,data,0,data.length);
		
		} catch(Exception ex) {
			System.out.println("### TRClassLoader.loadClass() - Exception: " + ex.toString());
			throw new ClassNotFoundException();
		}
		classes.put(className, c);
		return c;
	}

	public InputStream getResourceAsStream(String name)
	{
		InputStream is = ClassLoader.getSystemResourceAsStream(name);
		if(is != null) return is;
		try
		{
			String className = name.replace('.','/')+".class";
			is = new URL(urlString + className).openConnection().getInputStream();
		} catch (Exception e) {return null;}
		return is;
	}

	public URL getResource(String name)
	{
		URL url = ClassLoader.getSystemResource(name);
		if(url != null) return url;
		try
		{
			String className = name.replace('.','/')+".class";
			url = new URL(urlString + className);
		} catch (Exception e) {return null;}
		return url;
	}

}
