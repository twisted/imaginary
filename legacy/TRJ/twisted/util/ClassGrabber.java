package twisted.util;
import java.io.InputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Hashtable;
/**
 * This class allows for dynamic reloading of verbs in
 * twisted.reality.  Bits of it are hard-coded right now.  Not to be
 * taken orally.
 */

public class ClassGrabber extends ClassLoader
{
	private Hashtable classes = new Hashtable();
	/**
	 * Make a new ClassGrabber
	 */
	public ClassGrabber()
	{
		super();
		if(System.getSecurityManager() != null)
			System.getSecurityManager().checkCreateClassLoader();
	}
	
	/**
	 * Load or reload a class.  Needs to be fixed at some point to do
	 * network class loading.
	 */
	protected Class loadClass(String name, boolean b) throws ClassNotFoundException
	{
		Class c;
		
		// first, check the cache.
		c = (Class)classes.get(name);
		if (c != null) return c;
		
		//little hack to keep main classes from being loaded with this
		//classloader
		if (name.startsWith("java.") ||
			name.startsWith("javax.") ||
			((name.startsWith("twisted.reality.") && 
			  name.indexOf((int)'.', 16 /*"twisted.reality.".length()*/) == -1)
			 )
			)
		{
			return findSystemClass(name);
		}
		
		// now try loading it ourselves...if it doesn't work fall back to system loader.
		String fnm = name.replace('.','/')+".class";
		try
		{
			InputStream is;
			File ff =  new File(System.getProperty("user.dir"),fnm);
			is =new FileInputStream(ff);
			
			byte byt[];
			// note that this assumes that the whole file is available
			// immediately, which should always be true of local files
			// at least.
			byt = new byte[is.available()];
			is.read(byt);
			is.close();
			c = defineClass(name,byt,0,byt.length);
			if(b) resolveClass(c);
		}
		catch(IOException e)
		{
			return findSystemClass(name);
		}
		classes.put(name, c);
		return c;
	}
	
	public InputStream getResourceAsStream(String name)
	{
		return ClassLoader.getSystemResourceAsStream(name);
	}

	public java.net.URL getResource(String name)
	{
		return ClassLoader.getSystemResource(name);
	}

}
