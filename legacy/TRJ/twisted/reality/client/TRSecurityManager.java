package twisted.reality.client;

import java.net.URL;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.io.FileDescriptor;

/**
 * This class defines a security policy for Client-side extensions to TR
 * For code loaded from a class loader, the security manager
 * disables basically everything but AWT functions, clipboard access, and
 * ability to read/write from a Socket (but not create one).
 */
public class TRSecurityManager extends SecurityManager {
	
	/**
	 * Construct and initialize.
	 */
	public TRSecurityManager() {
	}
	
	/**
	 * True if called indirectly from a loaded class.
	 */
	private boolean inLoadedClass() {
		return inClassLoader();
	}
	
	/**
	 * Returns the security context (e.g., a URL).
	 */
	public Object getSecurityContext() {
		return null;
	}
	
	
	/**
	 * Loaded classes are not allowed to create class loaders, or even
	 * execute any of ClassLoader's methods.
	 */
	public synchronized void checkCreateClassLoader() {
		if (inLoadedClass()) {
			throw new TRSecurityException("classloader");
		}
	}
	
	/**
	 * Loaded classes are not allowed to manipulate threads.
	 */
	public synchronized void checkAccess(Thread t) {
		if (inLoadedClass()) {
			throw new TRSecurityException("thread");
		}
	}
	
	/**
	 * Loaded classes are not allowed to manipulate thread groups.
	 */
	public synchronized void checkAccess(ThreadGroup g) {
		if (inLoadedClass()) {
			throw new TRSecurityException("threadgroup");
		}
	}
	
	/**
	 * Loaded classes are not allowed to exit the VM.
	 */
	public synchronized void checkExit(int status) {
		if (inLoadedClass()) {
			throw new TRSecurityException("exit", String.valueOf(status));
		}
	}
	
	/**
	 * Loaded classes are not allowed to fork processes.
	 */
	public synchronized void checkExec(String cmd){
		if (inLoadedClass()) {
			throw new TRSecurityException("exec", cmd);
		}
	}
	
	/**
	 * Loaded classes are not allowed to link dynamic libraries.
	 */
	public synchronized void checkLink(String lib){
		switch (classLoaderDepth()) {
		case 2: // Runtime.load
		case 3: // System.loadLibrary
			throw new TRSecurityException("link", lib);
		default:
			break;
		}
	}
	
	/**
	 * Loaded classes are not allowed to access the system properties list.
	 */
	public synchronized void checkPropertiesAccess() {
		if (classLoaderDepth() == 2) {
			throw new TRSecurityException("properties");
		}
	}
	
	/**
	 * Loaded classes can access the system property named by <i>key</i>
	 * only if its twin <i>key.allow</i> property is set to true.
	 * For example, the property <code>java.home</code> can be read by
	 * loaded classes only if <code>java.home.allow</code> is <code>true</code>.
	 */
	public synchronized void checkPropertyAccess(String key) {
		if (classLoaderDepth() == 2) {
			if (!"true".equalsIgnoreCase(System.getProperty(key + ".allow"))) {
				throw new TRSecurityException("properties");
			}
		}
	}
	
	/**
	 * Check if a loaded class can read a particular file.
	 */
	public synchronized void checkRead(String file) {
		if (inLoadedClass())
			throw new TRSecurityException("file.read", file);
	}
	
	/**
	 * No file reads are valid from a loaded class.
	 * @exception  TRSecurityException If called from a loaded class.
	 */
	public void checkRead(String file, Object context) {
		if (inLoadedClass())
			throw new TRSecurityException("file.read", file);
	}
	
	/**
	 * Check if a loaded class can write a particular file.
	 * @exception  TRSecurityException If called from a loaded class.
	 */
	public synchronized void checkWrite(String file) {
		if (inLoadedClass()) {
			throw new TRSecurityException("file.write", file);
		}
	}
	
	/**
	 * Check if a file with the specified system dependent
	 * file name can be deleted.
	 * @param file the system dependent file name
	 * @exception  TRSecurityException If the file is not found.
	 */
	public void checkDelete(String file) {
		if (inLoadedClass()) {
			throw new TRSecurityException("file.delete", file);
		}
	}
	
	/**
	 * Loaded classes are not allowed to open descriptors for reading unless
	 * it is done through a socket, in which case other access
	 * restrictions still apply.
	 */
	public synchronized void checkRead(FileDescriptor fd) {
		if ((inLoadedClass() && !inClass("java.net.SocketInputStream"))
			|| (!fd.valid()) ) {
			throw new TRSecurityException("fd.read");
		}
	}
	
	/**
	 * Loaded classes are not allowed to open descriptors for writing unless
	 * it is done through a socket, in which case other access
	 * restrictions still apply.
	 */
	public synchronized void checkWrite(FileDescriptor fd) {
		if ( (inLoadedClass() && !inClass("java.net.SocketOutputStream")) 
			 || (!fd.valid()) ) {
			throw new TRSecurityException("fd.write");
		}
	}
	
	/**
	 * For now loaded classes can't listen on any port.
	 */
	public synchronized void checkListen(int port) {
		if (inLoadedClass()) {
			throw new TRSecurityException("socket.listen", String.valueOf(port));
		}
	}
	
	/**
	 * For now loaded classes can't accept connections on any port.
	 */
	public synchronized void checkAccept(String host, int port) {
		if (inLoadedClass()) {
			throw new TRSecurityException("socket.accept", host + ":" + String.valueOf(port));
		}
	}
	
	/**
	 * Checks to see if current execution context is allowed to use
	 * (join/leave/send/receive) IP multicast (disallowed from loaded classes).
	 */
	public void checkMulticast(InetAddress maddr) {
		if (inLoadedClass()) {
			throw new TRSecurityException("checkmulticast");
		}
	}
	
	/**
	 * Checks to see if current execution context is allowed to use
	 * (join/leave/send/receive) IP multicast (disallowed from loaded classes).
	 */
	public void checkMulticast(InetAddress maddr, byte ttl) {
		if (inLoadedClass()) {
			throw new TRSecurityException("checkmulticast");
		}
	}
	
	/**
	 * Loaded classes cannot make connections.
	 */
	public synchronized void checkConnect(String host, int port) {
		if (inLoadedClass()) {
			throw new TRSecurityException("checkConnect",
										  "To " + host + ":" + port);
		}
	}
	
	private synchronized void checkConnect(String fromHost, String toHost) {
		if (inLoadedClass()) {
			throw new TRSecurityException("checkConnect",
										  "To " + toHost);
		}
	}
	
	/**
	 * Loaded classes cannot make connections.
	 */
	public void checkConnect(String host, int port, Object context) {
		checkConnect(host, port);
	}
	
	/**
	 * Allow caller to create top-level windows.
	 * Allow loaded classes to create windows with warnings.
	 */
	public synchronized boolean checkTopLevelWindow(Object window) {
		if (inLoadedClass())
			return false;
		return true;
	}
	
	/**
	 * Check if a loaded class can access a package.
	 */
	public synchronized void checkPackageAccess(String pkg) {
		
		if (!inLoadedClass())
			return;
		int i = pkg.indexOf('.');
		
		while (i > 0) {
			String subpkg = pkg.substring(0, i);
			if (Boolean.getBoolean("package.restrict.access." + subpkg)) {
				throw new TRSecurityException("checkpackageaccess", pkg);
			}
			i = pkg.indexOf('.', i + 1);
		}
	}
	
	/**
	 * Check if a loaded class can define classes in a package.
	 */
	public synchronized void checkPackageDefinition(String pkg) {
		
		if (!inLoadedClass())
			return;
		int i = pkg.indexOf('.');
		
		while (i > 0) {
			String subpkg = pkg.substring(0, i);
			if (Boolean.getBoolean("package.restrict.definition." + subpkg)) {
				throw new TRSecurityException("checkpackagedefinition", pkg);
			}
			i = pkg.indexOf('.', i + 1);
		}
	}
	
	/**
	 * Check if a loaded class can set a networking-related object factory.
	 * (disallowed from loaded classes).
	 */
	public synchronized void checkSetFactory() {
		if (inLoadedClass()) {
			throw new TRSecurityException("cannotsetfactory");
		}
	}
	
	/**
	 * Disallow printing from loaded classes.
	 */
	public void checkPrintJobAccess() {
		if (inLoadedClass()) {
			throw new TRSecurityException("getPrintJob");
		}
	}
	
	/**
	 * Checks to see if an client can get access to the System Clipboard
	 * (allowed from loaded classes).
	 */
	public void checkSystemClipboardAccess() {
/*	allowed, at least for now.
	if (inLoadedClass()) {
	throw new TRSecurityException("checksystemclipboardaccess");
	}*/
		
	}
	
	/**
	 * Checks to see if an client can get access to the AWT event queue
	 * (disallowed from loaded classes).
	 */
	public void checkAwtEventQueueAccess() {
		if (inLoadedClass()) {
			throw new TRSecurityException("checkawteventqueueaccess");
		}
	}
	
	/**
	 * Check if client is allowed reflective access to a member or a set
	 * of members for the specified class.	Once initial access is granted,
	 * the reflected members can be queried for identifying information, but
	 * can only be <strong>used</strong> (via get, set, invoke, or
	 * newInstance) with standard Java language access control.
	 *
	 * <p>The policy is to dent <em>untrusted</em> clients access to
	 * <em>declared</em> members of classes other than those loaded via
	 * the same class loader.  All other accesses are granted.
	 */
	public void checkMemberAccess(Class clazz, int which) {
		if (which != java.lang.reflect.Member.PUBLIC) {
			ClassLoader currentLoader = currentClassLoader();
			if (currentLoader != null) {
				if (currentLoader != clazz.getClassLoader()) {
					throw new TRSecurityException("checkmemberaccess");
				}
			}
		}
	}
	
	/**
	 * Loaded classes cannot perform security provider operations.
	 */
	public void checkSecurityAccess(String provider) {
		if (inLoadedClass()) {
			throw new TRSecurityException("checksecurityaccess", provider);
		}
	}
}
