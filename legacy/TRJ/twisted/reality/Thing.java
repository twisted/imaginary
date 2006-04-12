package twisted.reality;

import java.util.Hashtable;
import java.util.Dictionary;
import java.util.Enumeration;
import java.util.Observable;
import java.util.Vector;
import twisted.util.LinkedList;
import twisted.util.StringLegalizer;
import twisted.util.BinaryTree;

/**
 * This class represents an object in the world of Twisted Reality.
 * The reason it's not called 'Object' is first of all, Thing sounds
 * so much cooler, but more importantly, Object is the base class of
 * all java objects.  Things have names, descriptions, properties
 * (which can be integers, booleans, other Things, dynamically created
 * Objects, or Strings). For example, a Sword would be a Thing. The
 * Sword would be a superclass to all sword-like things, and thus, in
 * the game, each time you wished to create a sword-like thing, you'd
 * type
 * 
 * <br> <code> <b>&gt;draw shiny sword</b> <br> You draw a shiny
 * sword.  <br> <b>&gt;extend shiny sword from Class_Sword</b> <br>
 * Successful subclassage.</code> <br> You now have a fully functional
 * sword.
 * 
 * @version 1.0.0, 1 Jul 1999
 * @author Glyph Lefkowitz
 */

public class Thing extends Nameable
{
	/**
	 * Creates a new Thing object, in a specified location, with a
	 * specified String as the name, and a specified String as the
	 * description.
	 *
	 * @param inLoc The Thing's location 
	 *
	 * @param inName The Thing's name 
	 *
	 * @param inDesc The Thing's description
	 */
	
	public Thing(Location inLoc, String inName, String inDesc)
	{
		this(inName,inDesc);
		ll=new twisted.util.LinkedList();
		myObservable=new twisted.util.LinkedList();
		place(inLoc);
		setGender('n');
	}
	
	twisted.util.LinkedList myObservable;
	
	/**
	 * Create a new thing with no arguments.  Used when reading from
	 * files.  If you create a Thing in this way, please remember to
	 * give it a name and put it somewhere, so it's not just sitting
	 * in the void!
	 */
	
	Thing()
	{
		this(null,null);
		ll=new twisted.util.LinkedList();
		myObservable=new twisted.util.LinkedList();
		setGender('n');
	}
	
	static Dictionary dict()
	{
		return new twisted.util.LinkedList();
	}
	
	/**
	 * Cause a player to observe this object.  (this is frequently
	 * called internally. It is unlikely that you will need to use
	 * it.)
	 *
	 * @param p the player which will observe this object.	
	 */
	
	void isObservedBy(Player p)
	{
		myObservable.addElement(p);
	}
	
	/**
	 * Recognize that a player's observation focus has been removed
	 * from this object.
	 *
	 * @param p The player which has ceased observing.
	 */
	
	void isNotObservedBy(Player p)
	{
		myObservable.remove(p);
	}
	
	/**
	 * Alert all players currently focused on this object that an
	 * event has occurred which changes it.	 (This is frequently used
	 * internally.	It is unlikely you will need to call it directly.
	 *
	 * @param r the event to relay
	 * this function now defunct.
	 *
	 * public void tellObservers(RealEvent r)
	 * {
	 * if(myObservable != null) myObservable.notifyObservers(r);
	 * }
	 */
	
	/**
	 * Set the description of this object.
	 *
	 * @param s The string to set the description to.
	 */
	
	public void describe(String s)
	{
		idescribe(s);
		//		tellObservers(new RealEvent("describe",s,this));
		focusRefreshMyObservers();
	}
		
	/**
	 * Sets the 'theme' of the objects, so that all players looking at
	 * said object will see a certain motif of colors and/or graphics
	 * upon walking through this room or section of the map.
	 *
	 * @param s The name of the theme to be set.
	 */
	
	public void setTheme(String s)
	{
		String si = Age.intern(s);
		theme=si;
		if(myObservable!=null) synchronized(myObservable)
		{
			Enumeration e = myObservable.elements();
			while(e.hasMoreElements())
			{
				Player p = (Player) e.nextElement();
				if(p.user!=null) p.user.theme(si);
			}
		}
	}
	
	/**
	 * Gets the current theme of this thing.
	 */
	public String getTheme()
	{
		if( (place()!=null) && ((theme==null) || (theme.equals("default"))) )
		{
			return place().getTheme();
		}
		return theme;
	}
	
	String theme;
	char gender;
	
	/**
	 * Determine the gender of this object.	 Currently available
	 * genders are 'm', 'f', and 'n'
	 *
	 * @return 'm' 'f' or 'n'
	 */
	
	public final char getGenderTo(Thing t)
	{
		return gender;
	}
	
	/**
	 * Set the gender of this object or person.
	 *
	 * @param c The gender to set to. Currently available genders are
	 * 'm', 'f', and 'n' (if these are not obvious to you, you need
	 * more help than some online documentation can give.
	 */
	
	public final void setGender(char c)
	{
		gender=c;
	}
	
	/**
	 * Returns the string "him", "her", or "it" depending upon the
	 * gender of this object.
	 */
	
	final String himher()
	{
		switch(gender)
		{
		case 'm':
			return "him";
			
		case 'f':
			return "her";
		}
		return "it";
	}
	
	/**
	 * Returns the string "Him", "Her", or "It" depending upon the
	 * gender of this object.
	 */
	
	final String HimHer()
	{
		switch(gender)
		{
		case 'm':
			return "Him";
			
		case 'f':
			return "Her";
		}
		return "It";
	}
	
	/**	 
	 * Returns the string "his ", "her ", or "its ", depending upon
	 * the gender of this object.  
	 * @return "his " or "her "
	 */
	
	final String hisher()
	{
		switch(gender)
		{
		case 'm':
			return "his";
			
		case 'f':
			return "her";
		}
		return "its";
	}
	
	/**	  
	 * Returns the string "His ", "Her ", or "Its " depending upon
	 * the gender of this object.
	 * 
	 * @return "His ", "Her ", or "Its "
	 */
	
	final String HisHer()
	{
		switch(gender)
		{
		case 'm':
			return "His";
			
		case 'f':
			return "Her";
		}
		return "Its";
	}
	
	/**
	 * Returns the string "he", "she", or "it", depending upon the
	 * gender of this object.
	 *
	 * @return "he" "she" or "it"
	 */
	
	final String heshe()
	{
		switch(gender)
		{
		case 'm':
			return "he";
		case 'f':
			return "she";
		}
		return "it";
	}
	
	/**
	 * Returns the string "he", "she", or "it" depending upon the
	 * gender of this object.
	 */
	
	final String HeShe()
	{
		switch(gender)
		{
		case 'm':
			return "He";
		case 'f':
			return "She";
		}
		return "It";
	}
	
	/**
	 * Tells this object to handle an event that you have generated.
	 * @param e The event to handle.
	 */
	
	public synchronized void handleEvent(RealEvent e)
	{
		RealEventHandler r = _getHandler(e.type());
		if(r != null)
		{
			try
			{
				r.gotEvent(e,this);
			}
			catch(Throwable th)
			{
				Age.log("Exception occurred during event dispatching: "+th);
			}
		}
	}
	
	/**
	 * Tells this object to handle an event.
	 * 
	 * @param eventTitle The event type to invoke
	 * 
	 * @param eventArgument The arbitrary data to pass to the handler
	 * of this event.
	 *
	 * @param eventOrigin The object that should be recognized as
	 * initiating this event.
	 */
	
	public synchronized void handleEvent(String eventTitle,
										 Object eventArgument,
										 Thing eventOrigin)
	{
		handleEvent(new RealEvent(eventTitle,eventArgument,eventOrigin));
	}
	
	/**
	 * Handles an event delayed by the given amount of time.  Note -
	 * the soonest an event can happen is one game 'tick' later, or
	 * 10*pi seconds.  It is not garuanteed to happen then, either, it
	 * might take considerably longer, depending on the number of
	 * events that are scheduled to happen...
	 * 
	 * <BR> Note - the thread which runs all events checks for new
	 * events every e seconds.
	 *
	 * @param e The event to be scheduled
	 *
	 * @param a The amount of time to wait, in game ticks (10*pi
	 * seconds)  The range of this argument is 1-MAX_INT.
	 */
	
	public void handleDelayedEvent(RealEvent e, int a)
	{
		Age.theUniverse().installDelayedEvent(e,a,this,false);
	}
	
	/**
	 * Adds an handler for the specified event type.
	 *
	 * @param eventTitle The type of event to handle.
	 * @param classname The classname of the event handler being added.
	 *
	 * @throws ClassNotFoundException if the class 'classname' could not be loaded.
	 */
	
	public void putHandler(String eventTitle, String classname) throws ClassNotFoundException
	{
		if(eventhandlers==null) eventhandlers = dict();
		RealEventHandler r=Age.theUniverse().loadEvent(classname);
		eventhandlers.put(Age.intern(eventTitle),Age.intern(classname));
	}
	
	/**
	 * Removes an event handler for the specified event type.
	 * 
	 * @param eventTitle the type of event to remove the handler for.
	 */
	
	public void removeHandler(String eventTitle)
	{
		if(eventhandlers == null) return;
		eventhandlers.remove(eventTitle);
		if (eventhandlers.isEmpty())
			eventhandlers=null;
	}
	
	/**
	 * Gets the class that handles a particular event on this thing
	 * @param eventTitle the event-type to get
	 * @returns a string containing the class-name of the handler.
	 */
	
	public String getHandler(String eventTitle)
	{
		String v = null;
		
		if (eventhandlers != null)
			v = (String) eventhandlers.get(eventTitle);
		
		if(v == null && superclass != null && superclass.sThing() != null)
		{
			v=superclass.sThing().getHandler(eventTitle);
		}
		
		return v;
	}
	
	/**
	 * Internal function for getting the handler loaded.  
	 */
	
	RealEventHandler _getHandler(String eventTitle)
	{
		try
		{
			String s = getHandler(eventTitle);
			if(s != null)
				return Age.theUniverse().dynLoadEvent(s);
		} catch (ClassNotFoundException e) {
			Age.log("Error using RealEventHandler: " + e);
		}
		return null;
	}
	
	private Dictionary props;
	
	/**
	 * Adds a dynamic property to this object. The dynamic property is
	 * accessed via the normal getString/getInt/etc methods, and from
	 * external appearances is indistinguishable from a static
	 * property.
	 *
	 * @param name The name of the property.
	 * @param className The classname of the dynamic property to be loaded.
	 * 
	 * @throws ClassNotFoundException if the class 'className' could
	 * not be loaded.
	 */
	
	public void putDynProp(String name, String className)
		throws ClassNotFoundException
	{
		putProp(name,new DynPropWrap(Age.intern(className)));
	}
	
	/**
	 * Generically puts a property onto any object.
	 *
	 * @param key The key, or name, of the property being stored.
	 *
	 * @param val The object being stored as a property.
	 */
	
	void putProp(String key, Object val)
	{
		String in_key = Age.intern(key);
			
		if(val instanceof String)
			val = Age.intern((String)val);
		if(props == null) props=dict();
		
		if (in_key!= null && val !=null)
		{
			props.put(in_key,val);
			if(in_key.equals("name") && (loc != null))
			{
				loc.updateNameFor(this);
			}
			else if (in_key.equals("description"))
			{
				focusRefreshMyObservers();
			}
		}
	}
	
	/**
	 * Put a persistable data-structure onto this object.  Builtin
	 * persistable data structures in this version of Twisted Reality
	 * are:
	 *
	 * <ul>
	 * <li>Stack
	 * </ul>
	 *
	 * It is also possible to write your own (they will be implicitly
	 * loaded when they are referenced from a Verb, DynamicProperty,
	 * or EventHandler, and explicitly loaded when read in from the
	 * map, so don't worry about it.
	 *
	 * @param name the name of the property.
	 * @param val the persistable to add.
	 * 
	 * @see twisted.reality.Stack
	 */
	
	public void putPersistable(String name, Persistable val)
	{
		putProp(name,val);
	}
	
	/**
	 * This is useful for a retrieving a complex data structure (Such
	 * as a Stack, List, or Vector) which had previously been stored
	 * on an object.  This is the recommended way to call it as it
	 * takes into account the source of the request for this
	 * information.	 <br> <br> (If you do not understand this, do not
	 * use this function.  It is provided for veteran programmers
	 * working with complex data structures, not people writing simple
	 * scripted actions)
	 * 
	 * @param name The name of the persistable property to look for
	 * 
	 * @param who The Thing (or Player, or Room) requesting the information
	 */
	
	public Persistable getPersistable(String name,Thing who)
	{
		Object o = getProp(name,who);
		if (o instanceof Persistable)
			return ((Persistable) o);
		
		return null;
	}

	/** 
	 * This is useful for a retrieving a complex data structure (Such 
	 * as a Stack, List, or Vector) which had previously been stored 
	 * on an object.  <br> <br> (If you do not understand this, do not 
	 * use this function.  It is provided for veteran programmers 
	 * working with complex data structures, not people writing simple 
	 * scripted actions) 
	 *
	 * @param name The name of the persistable property to look for
	 */ 
	
	public Persistable getPersistable(String name)
	{
		return getPersistable(name,this);
	}
	
	/**
	 * Gets a property and returns it generically, as an Object.
	 * The possible choices for the type are Integer, Boolean, and
	 * String.
	 *
	 * @param key The key, or name, of the property being searched for.
	 */
	
	Object getProp(String key)
	{
		Object rtrn;
		rtrn=null;
		if (props != null)
		{
			rtrn=props.get(key);
		}
		
		if (rtrn!=null) return rtrn;
		
		Thing t = ((superclass==null)?null:superclass.sThing());
		
		if( (t != null) && (t != this) )
		{
			return t.getProp(key);
		}
		return null;
	}
	
	/**
	 * gets a property and returns it generically.
	 *
	 * @param key The key of the property
	 *
	 * @param who The Thing retrieving it.
	 */
	Object getProp(String key, Thing who)
	{
		Object o=getProp(key);
		if(o!=null)
		{
			if(o instanceof DynamicProperty)
			{
				return ( (DynamicProperty)o).value(this, who);
			}
			else
			{
				return o;
			}
		}
		return null;
	}
	
	/**
	 * Removes a property from this Thing.
	 * @param name the property to remove.
	 */
	
	public void removeProp(String name)
	{
		if (props==null) return;
		props.remove(name);
		/* garbage collect unused tables */
		if (props.isEmpty())
			props=null;
	}
	
	/**
	 * Checks to see if the named property exists on this Thing.
	 * @param name the property to check.
	 */ 
	
	public boolean hasProp(String name)
	{
		return (getProp(name)!=null);
	}

	/**
	 * Checks to see if property name is a dynamicProperty.
	 *
	 * @param name the property to check.
	 * 
	 * @returns true if it is a dynamic property, false if it is a
	 * static property or nonexistant.
	 */
	public boolean isPropertyDynamic(String name)
	{
		return (getProp(name) instanceof DynamicProperty);
	}

	/**
	 * Creates or changes an Integer property on this Thing.
	 * 
	 * @param name The name of the property being stored.
	 * 
	 * @param val The value being stored.
	 */
	
	public void putInt(String name, int val)
	{
		putProp(name,new Integer(val));
	}
	
	/**
	 * Retrieves and returns an Integer property on this Thing.
	 * This is the preferred way to call this method, as it provides
	 * a perspective from which to request the property.
	 *
	 * @param name The name of the property being retrieved.
	 * 
	 * @param who The Thing requesting this property.
	 */
	
	public int getInt(String name,Thing who)
	{
		Object f = getProp(name,who);
		if(f instanceof Number)
		{
			return ((Number) f).intValue();
		}
		return 0;
	}
	
	/**
	 * Retrieves and returns an Integer property on this Thing.
	 *
	 * @param name The name of the property being retrieved.
	 */
	
	public int getInt(String name)
	{
		Object f = getProp(name);
		if(f instanceof Number)
		{
			return ((Number) f).intValue();
		}
		return 0;
	}
	
	/**
	 * Stores a Long Integer property on this Thing.
	 * 
	 * @param name The name of the property being stored.
	 *
	 * @param val The value being stored.
	 */
	
	public void putLong(String name, long val)
	{
		putProp(name,new Long(val));
	}
	
	
	/**
	 * Retrieves and returns a Long Integer property on this Thing.
	 * This is the preferred way to call this method, as it provides
	 * a perspective from which to request the property.
	 *
	 * @param name The name of the property being retrieved.
	 *
	 * @param who The Thing requesting this property.
	 */
	
	public long getLong(String name,Thing who)
	{
		Object f = getProp(name,who);
		if(f instanceof Number)
		{
			return ((Number) f).longValue();
		}
		return 0;
		// Should probably throw a NoSuchElementException or something...
	}
	
	/**
	 * Retrieves and returns a Long Integer property on this Thing.
	 *
	 * @param name The name of the property being retrieved.
	 */
	public long getLong(String name)
	{
		return getLong(name,this);
	}
	
	/**
	 * Creates or changes a Float property on this Thing.
	 *
	 * @param name The name of the property being stored.
	 *
	 * @param val The value being stored.
	 */
	
	public void putFloat(String name, float val)
	{
		putProp(name,new Float(val));
	}
	
	
	/**
	 * Retrieves and returns a Float property on this Thing.
	 * This is the preferred way to call this method, as it provides
	 * a perspective from which to request the property.
	 *
	 * @param name The name of the property being retrieved.
	 *
	 * @param who The Thing requesting this property.
	 */
	
	public float getFloat(String name,Thing who)
	{
		Object f = getProp(name,who);
		if(f instanceof Number)
		{
			return ((Number) f).floatValue();
		}
		return 0;
	}
	
	/**
	 * Retrieves and returns a Float property on this Thing.
	 *
	 * @param name The name of the property being retrieved.
	 */
	
	public float getFloat(String name)
	{
		Object f = getProp(name);
		if(f instanceof Number)
		{
			return ((Number) f).floatValue();
		}
		return 0;
	}
	
	/**
	 * Stores a String property on this Thing, which can be retrieved
	 * with getString.
	 *
	 * @param name The name of the property being stored.
	 *
	 * @param val The value being stored.
	 */
	
	public void putString(String name, String val)
	{
		putProp(name,val);
	}
	
	/**
	 * Places an objet array as a String property, which, when
	 * retrived with respect to a player (using
	 * getString(Thing,Thing)) will return the appropriate
	 * perspectivized String.  This can also be retrieved raw with
	 * getObjects(String).  DO NOT pass Objects other than Strings,
	 * Things, and Perceptibles to this function!  There may be
	 * unexpected effects, and it will undoubtedly damage your
	 * mapfile.
	 */
	
	public void putString(String name, Object[] val)
	{
		putProp(name,val);
	}

	public void putString(String name, Vector val)
	{
		putString(name,fromVector(val));
	}
	
	/**
	 * A simple utility method to convert a Vector to an Object[].
	 * This allocates the Object[].
	 */
	
	public static final Object[] fromVector(Vector v)
	{
		Object[] mObject = new Object[v.size()];
		v.copyInto(mObject);
		return mObject;
	}
	
	/**
	 * This function evaluates all the Perceptibles in the array
	 * s and concatanates all the resulting strings.
	 * 
	 * @see twisted.reality.Perceptible
	 */
	public String fromMyPerspective(Object x)
	{
		if (!(x instanceof Object[]))
		{
			return String.valueOf(x);
		}
		Object[] s = (Object[]) x;
		StringBuffer tapt=new StringBuffer();
		for (int i = 0; i<s.length; i++)
		{
			if (s[i] instanceof Thing)
			{
				// reasonable default
				if (i==0)
					s[i]=Name.Of((Thing)s[i]);
				else
					s[i]=Name.of((Thing)s[i]);
			}
			if (s[i] instanceof Perceptible)
			{
				tapt.append( ((Perceptible)s[i]).toStringTo(this) );
			}
			else /* if (s[i] instanceof String) or Object */
			{
				tapt.append(s[i]);
			}
		}
		return tapt.toString();
	}
	
	/**
	 * Retrieves and returns a String property on this Thing.
	 * This is the preferred way to call this method, as it provides
	 * a perspective from which to request the property.
	 *
	 * @param name The name of the property being retrieved.
	 * 
	 * @param who The Thing requesting this property.
	 */
	
	public String getString(String name, Thing who)
	{
		Object f = getProp(name,who);
		String retr;
		if (f instanceof String)
		{
			retr=(String)f;
		}
		else if (f instanceof Object[])
		{
			retr = who.fromMyPerspective(f);
		}
		else
		{
			retr = null;
		}
		return retr;
	}
	
	/**
	 * This method is for programmatic retrieval of Object arrays
	 * placed with the putString(String,Object[]) method.  This can be
	 * useful for storing a perspective-dependant pseudo-String
	 * property which needs to eventually become a descriptive
	 * element.
	 */
	
	public Object[] getObjects(String name)
	{
		Object zzz = getProp(name,this);
		if (zzz instanceof Object[])
		{
			return (Object[])zzz;
		}
		return null;
	}
	
	/**
	 * Retrieves and returns a String property on this Thing, without
	 * taking a perspective into account.
	 *
	 * @param name The name of the property being retrieved.
	 */
	
	public String getString(String name)
	{
		Object f = getProp(name);
		String retr;
		if (f instanceof String)
		{
			retr=(String)f;
		}
		else
		{
			retr = null;
		}
		return retr;
	}
	
	/**
	 * Stores a boolean property on this Thing, which can be retrieved
	 * with getBool.
	 *
	 * @param name The name of the property being stored.
	 *
	 * @param val The value being stored.
	 */
	
	public void putBool(String name, boolean val)
	{
		putProp(name,new Boolean(val));
	}
	
	/**
	 * Retrieves and returns a Boolean property on this Thing.
	 * This is the preferred way to call this method, as it provides
	 * a perspective from which to request the property.
	 *
	 * @param name The name of the property being retrieved.
	 * @param who The Thing requesting this property.
	 */
	
	public boolean getBool(String name, Thing who)
	{
		Object f = getProp(name, who);
		
		if (f instanceof Boolean)
		{
			return ((Boolean) f).booleanValue();
		}
		return false;
	}
	
	/**
	 * Gets a boolean property from this Thing, without taking a
	 * perspective into account.
	 *
	 * @param name The name of the property to retrieve.
	 */
	
	public boolean getBool(String name)
	{
		Object f = getProp(name);
		
		if (f instanceof Boolean)
		{
			return ((Boolean) f).booleanValue();
		}
		return false;
	}
	
	/**
	 * Creates or changes a Thing property on this Thing, which
	 * can be retrieved with getThing.
	 *
	 * @param name the Key, or name, of the property being stored.
	 * 
	 * @param val The Thing being stored (linked to). 
	 */
	
	public void putThing(String name, Thing val)
	{
		if(val!=null)
			putProp(name, val.ref );
	}
	
	/**
	 * Returns this thing's identifier. The identifier is like
	 * a handle to the thing. It allows things that are only referenced
	 * by properties to be removed.
	 */
	
	public ThingIdentifier identifier()
	{
		return ref;
	}
	ThingIdentifier ref;
	
	/**
	 * Retrives and returns a Thing property on this Thing.	 
	 * This is the preferred way to call this method, as it provides
	 * a perspective from which to request the property.
	 *
	 * @param name The name of the Thing property to retrieve
	 * 
	 * @param who The thing requesting this information
	 */
	
	public Thing getThing(String name, Thing who)
	{
		Object f = getProp(name, who);
		
		if(f instanceof ThingIdentifier)
		{
			ThingIdentifier F = (ThingIdentifier) f;
			if(F.sThing()==null)
			{
				removeProp(name);
				return null;
			}
			else
			{
				return F.sThing();
			}
		}
		// This is a utility for people returning Things from
		// DynamicPropertys
		else if (f instanceof Thing)
		{
			return ((Thing) f);
		}
		return null;
	}
	/** 
	 * Retrives and returns a Thing property on this Thing without
	 * taking a perspective into account.
	 * 
	 * @param name The name of the Thing property to retrieve 
	 */
	public Thing getThing(String name)
	{
		Object f = getProp(name);
		
		if(f instanceof ThingIdentifier)
		{
			ThingIdentifier F = (ThingIdentifier) f;
			if(F.sThing()==null)
			{
				removeProp(name);
				return null;
			}
			else
			{
				return F.sThing();
			}
		}
		return null;
	}
	
	/**
	 * Names this Thing, and adds it to the global list of Things in
	 * the current universe.  If the object is being renamed, it
	 * removes itself initially, then re-adds itself.
	 *
	 * @param s The new name of the Thing. 
	 */
	
	public void name(String s)
	{
		String truenm=s;
		int i = 0;
		Location myPlace = place();
		if (s.equals(""))
			truenm="blank object";
		place(null);
		if ((ll != null ) && (ll.get(truenm)!=null)) /* test needed for dynamic object creation */
		{
			throw new IllegalArgumentException("Sorry, can't name an object after one of its own synonyms.");
		}
		
		if(NAME()!=null) Age.theUniverse().removeSyn(this);
		
		super.name(null);
		if(s!=null)
			if(s.indexOf("'s") != -1)
				posessive=true; 
			else 
				posessive=false;
		while(Age.theUniverse().findThing(truenm)!=null)
		{
			truenm=s+"("+ ++i +")";
		}
		
		super.name(truenm);
		
		if(ref == null)
		{
			ref=Age.theUniverse().findIdentifier(truenm);
			if(ref.t!=null && ref.t!=this)
			{
				ref=new ThingIdentifier();
			}
			ref.t=this;
		}
		
		if (NAME() != null) Age.theUniverse().addSyn(this);
		place(myPlace);
		
		focusRefreshMyObservers();
	}
	
	/**
	 * Returns the name of this thing.  (Note - the value this returns
	 * can be changed by adding a string property called "name")
	 */
	
	public String name()
	{
		String s = getString("name");
		
		if(s != null)
		{
			return s;
		}
		return super.name();
	}
	
	/**
	 * Returns the name of this thing, as a given Thing (usually a
	 * player) would percieve it.  (Note - This is useful when the
	 * property 'name' is a dynamic property and can vary depending on
	 * the viewer.)
	 *
	 * @param p The thing who is observing this Thing.
	 */
	
	public String nameTo(Thing p)
	{
		String s = getString("name",p);
		if(s!=null) return s;
		
		/*if(p==this)
		  return "you";*/
		
		return name();
	}
	
	/**
	 * Returns the description of this thing, as a given Thing
	 * (usually a player) would percieve it.
	 *
	 * (Note - This is useful when the property 'description' is a dynamic
	 * property and can vary depending on the viewer.)
	 * There is another method, "describe()", which
	 * will just return the object's description)
	 * 
	 * @param p The thing who is requesting this Thing's description.
	 * 
	 */
	
	String describeTo(Thing p)
	{
		String s = getString("description",p);
		if(s!=null) return s;
		return describe();
	}
	
	/**
	 * The full description of this object, as the game would render
	 * it to a given observer *p* at the time that it is requested.
	 */
	
	public String fullyDescribeTo(Thing p)
	{
		StringBuffer sb = new StringBuffer(describeTo(p));
		Enumeration theE = descriptionElements();
		if(theE!=null)
		{
			while(theE.hasMoreElements())
			{
				String theO = p.fromMyPerspective(theE.nextElement());
				sb.append(" ").append(theO);
			}
		}
		return sb.toString();
	}

	String mood;
	
	/**
	 * This sets the mood of the object to a given string. The mood of
	 * an object is what appears in the inventory box - for instance,
	 * an object whose mode is "beeping" would be displayed as "There
	 * is a foo here, beeping.".  If the mood is set to null, there
	 * will be nothing displayed there.	 A person whose mood is "sad"
	 * will be displayed as "Steve is here, sad.".	Therefore, moods
	 * such as "sitting", "standing", "beeping", and "blinking" can be
	 * used to indicate an object's status.
	 *
	 * @param s The string to set the mood to
	 */
	
	public void mood(String s)
	{
		mood=s;
		Location myPlace=place();
		place(myPlace);
	}

	/**
	 * Retrieves the mood of the object.
	 *
	 * @see mood(String)
	 * @return the current mood
	 */
	
	public String moodTo(Thing t)
	{
		return mood();
	}
	
	
	String mood()
	{
		return mood;
	}
	
	/**
	 * A utility var to remember if this thing's name has an "'s" in it.
	 */
	
	boolean posessive;

	String getPrepTo(Thing t)
	{
		String realPrep = getString("object preposition",t);
		if (realPrep == null)
		{
			realPrep = loc.getString("preposition",t);
			if (realPrep == null)
				realPrep="in";
		}
		return realPrep;
	}
	
	/**
	 * This function creates the display string for this object.  It
	 * displays the string 'There is a(n) ' (whatever) ' here.',
	 * ususally.
	 *
	 * @return "A[n] <name> is here[, <mood>].", or, if the object
	 * belongs to some character, "<charname>'s <whatever> is here[,
	 * <mood>].".
	 */
	
	String isHereTo(Thing t)
	{
		StringBuffer sb;
		if ((loc != null) && (loc.isBroadcast()))
		{
			String realPrep = getPrepTo(t);
			return AAn()+nameTo(t) + " is "+realPrep+" "+loc.the()+loc.nameTo(t)+((moodTo(t) != null)?", "+moodTo(t)+'.' : ".");
		}
		else
			return AAn()+nameTo(t) + " is here" + ((moodTo(t)!=null) ? ", "+moodTo(t)+'.' : ".");
	}
	
	/**
	 * Returns the correct definite article, lowercase, for this
	 * object.	Please note that the article has a space after it
	 * - ie, "Take "+fish.the()+fish.name()+" please!" if fish
	 * is an object actually called "fish" will return "Take the fish,
	 * please!"	 wheras if it's a person named "john", it'll come out
	 * "Take John, please!".
	 * 
	 * @return "the "
	 */
	
	String the()
	{
		String tv = getString("the");
		if(tv != null)
			return tv;
		return "the ";
	}
	
	/**
	 * Returns the correct definite article, uppercase, for this object.
	 *
	 * @return "The "
	 */
	
	String The()
	{
		String tv = getString("the");
		if(tv != null)
			return (Character.toUpperCase(tv.charAt(0)) + tv.substring(1));
		return "The ";
	}
	
	/**
	 * Returns the lowercase indefinite article for this object.
	 * Usually returns either "a " or "an " depending on the first
	 * letter of the Thing's name, but it can be overridden with
	 * the string property 'aan'.
	 *
	 * @return the proper indefinite article
	 */
	
	final String aan()
	{
		String tv = getString("aan");
		if(tv != null)
		{
			return tv;
		}
		return aan(name());
	}
	
	/**
	 * Returns the capitalized indefinite article for this object.
	 * Usually returns either "A " or "An " depending on the first
	 * letter of the Thing's name, but it can be overridden with
	 * the string property 'aan'. (the first letter of the property
	 * is automatically capitalized)
	 *
	 * @return the proper indefinite article
	 */
	
	final String AAn()
	{
		// is this really necessary?
		String tv = getString("aan");
		if(tv != null)
		{
			return (Character.toUpperCase(tv.charAt(0)) + tv.substring(1));
		}
		return AAn(name());
	}
	
	/**
	 * Returns the lowercase indefinite article (a, an) for the given String.
	 */
	
	public static final String aan(String s)
	{
		char x = s.charAt(0);
		
		return (
				(( x == 'a')
				 ||
				 (x == 'e')
				 ||
				 (x == 'i')
				 ||
				 (x == 'o')
				 ||
				 (x == 'u')
				 ||
				 (x == 'A')
				 ||
				 (x == 'E')
				 ||
				 (x == 'I')
				 ||
				 (x == 'O')
				 ||
				 (x == 'U'))
				? "an " : "a "
				);
	}
	
	/**
	 * Returns the uppercase indefinite article (a, an) for the given String.
	 */
	public static final String AAn(String s)
	{
		char x = s.charAt(0);
		
		return (
				(( x == 'a')
				 ||
				 (x == 'e')
				 ||
				 (x == 'i')
				 ||
				 (x == 'o')
				 ||
				 (x == 'u')
				 ||
				 (x == 'A')
				 ||
				 (x == 'E')
				 ||
				 (x == 'I')
				 ||
				 (x == 'O')
				 ||
				 (x == 'U'))
				? "An " : "A "
				);
	}
	
	/**
	 * This function moves the object to a new location.  This is NOT
	 * the 'take' verb in a function - it completely ignores all
	 * properties of an object and zips it to wherever you specify.
	 * Do not always call this function when you want to move
	 * something - most of the time, moveTo should be adequate.
	 * 
	 * This method sends the following events:<br>
	 * <blockquote>
	 * The Contents of the starting Location see Thing leave
	 * <br>
	 * The starting Location itself sees Thing leave
	 * <br>
	 * Contents of the destination Location see Thing arrive 
	 * <br>
	 * The destination Location itself sees Thing arrive
	 * <br>
	 * Thing sees itself move from Starting to Destination Location
	 * </blockquote>
	 * @param where The new location to be moved to.  */
	
	public synchronized void place(Location where)
	{
		RealEvent re;
		Enumeration othings;
		Location myOldLoc=loc;
		loc=where;
		
		if (myOldLoc != null)
		{
			othings = myOldLoc.things(true,true);
			re = new RealEvent("leaving",loc,this);

			// Things in the Location see it leave
			
			while(othings.hasMoreElements())
			{
				Thing t = (Thing) othings.nextElement();
				if (t == this) continue;
				t.handleEvent(re);
			}
			
			re=new RealEvent ("leave",loc,this);

			// The Location itself sees it leave
			
			myOldLoc.handleEvent(re);
			
			myOldLoc.toss(this);
			
			// If the Object was visible, make all the players not
			// look at it anymore... It's gone.

			if (myObservable != null)
			{
				synchronized(myObservable)
				{
					Enumeration e = myObservable.elements();
					while(e.hasMoreElements())
					{
						Player p = (Player)e.nextElement();
						Location l = p.topPlace();
						p.setFocus(l);
					}
				}
			}
		}
		
		if (where != null)
		{
			where.grab(this);
			where.updateNameFor(this);

			othings = where.things(true,true);
			re = new RealEvent("entering",loc,this);

			// Things in the destination Location see it arrive
			
			while(othings.hasMoreElements())
			{
				Thing t = (Thing) othings.nextElement();
				if (t == this) continue;
				t.handleEvent(re);
			}

			// The destination Location itself sees it arrive
			
			re = new RealEvent("enter",loc,this);
			where.handleEvent(re);
		}

		// The Thing being moved is informed of the movement
		
		re = new RealEvent("place",myOldLoc,where);
		handleEvent(re);
	}
	
	/**
	 * Tell object's observers to re-load its state (name,
	 * description, contained objects, etc).
	 */
	
	public void focusRefreshMyObservers()
	{
		if(myObservable!=null) synchronized(myObservable)
		{
			Enumeration e = myObservable.elements();
			while(e.hasMoreElements())
			{
				Player p = (Player) e.nextElement();
				p.focusRefresh();
			}
		}
	}

	/**
	 * Moves the object to a new location with place() if that is
	 * allowed.
	 *
	 * @param where The new location to move to.
	 *
	 * @param s The string to announce the leaving and arrival of the
	 * Thing.
	 *
	 * @return whether the move succeeded.
	 */
	
	public boolean moveTo(Location where, Object[] s)
	{
		return moveTo(where,s,s);
	}
	
	/**
	 * Moves the object to a new location with place() if that is
	 * allowed.
	 *
	 * @param where Where do you want to go today?
	 *
	 * @param leave What do you have to say before you go?
	 *
	 * @param arrive What do you want to say when you get there?
	 *
	 * @return whether the move succeeded.
	 */
	
	public boolean moveTo(Location where, Object[] leave, Object[] arrive)
	{
		if(isComponent()) 
			return false;
		
		Location l = loc;
		place(where);
		if(l!=null)
		{
			synchronized(l.myObservable)
			{
				Enumeration e = l.myObservable.elements();
				while(e.hasMoreElements())
				{
					Player p = (Player) e.nextElement();
					p.notifyLeaving(this,leave);
				}
			}
			if ((l.loc!=null)&&(l.isBroadcast()))
			{
				synchronized(l.loc.myObservable)
				{
					Enumeration e = l.loc.myObservable.elements();
					while(e.hasMoreElements())
					{
						Player p = (Player) e.nextElement();
						p.notifyLeaving(this,leave);
					}
				}
			}
		}
		if(loc != null)
		{
			synchronized(loc.myObservable)
			{
				Enumeration e = loc.myObservable.elements();
				while(e.hasMoreElements())
				{
					Player p = (Player) e.nextElement();
					p.notifyEntering(this,arrive);
				}
			}
			if ((loc.loc!=null) && (loc.isBroadcast()))
			{
				synchronized(loc.loc.myObservable)
				{
					Enumeration e = loc.loc.myObservable.elements();
					while(e.hasMoreElements())
					{
						Player p = (Player) e.nextElement();
						p.notifyEntering(this,leave);
					}
				}
			}
		}
		if(loc==where)
		{
			return true;
		}
		return false;
	}
	
	/**
	 * Returns the current location of the object.
	 */
	
	public final Location place()
	{
		/*if(loc!=null) if (loc.furniture)
		{
			return loc.place();
			}*/
		return loc;
	}
	
	/**
	 * This is the location that the thing is in after going outside
	 * all 'broadcast' locations.  For example, if this Thing is a
	 * book placed on a chair, this will represent the room that the
	 * chair is in.
	 */
	
	public final Location topPlace()
	{
		Location ezlar;
		ezlar = place();
		while ((ezlar != null) && (ezlar.isBroadcast()))
		{
			ezlar=ezlar.place();
		}
		return ezlar;
	}

	/**
	 * This is the "first" Room that the thing is in after recursing
	 * up through any Locations it occupies. This doesn't care whether
	 * the locations are closed/broadcast/whatever, it just stops at
	 * the first available room.
	 **/

	public final Location topRoom()
	{
		Location ezlar;
		ezlar = place();
		while ((ezlar != null) && (!(ezlar instanceof Room)))
		{
			ezlar=ezlar.place();
		}
		return ezlar;
	}

	/**
	 * This is the outermost Location that the thing is in after recursing
	 * up through any and all Locations it occupies.
	 **/

	public final Location topLocation()
	{
		Location ezlar;
		ezlar = place();
		while ((ezlar != null))
		{
			ezlar=ezlar.place();
		}
		return ezlar;
	}

	/**
	 * Gets a verb from the object's list of current verbs.
	 *
	 * @param key The name (ie, take, drop, frotz) to get.
	 * 
	 * @return	the Verb associated with the name, or null if the verb
	 *			is non-existant on this player.
	 */
	
	public final Verb getVerb(String key)
	{
		String c;
		// if this object has the verb x, get the class
		try
		{
			if (verbs != null && (c =(String) verbs.get(key)) != null)
				return Age.theUniverse().dynLoadVerb(c);
		} catch (ClassNotFoundException e) {
			Age.log("Error using Verb " + key + ": " + e);
			// return null;
		}

		// otherwise ask the super
		if (superclass != null && superclass.sThing() != null)
			return superclass.sThing().getVerb(key);
			
		// hm, no super, and no ability of that name here, return null
		return null;
	}
	
	/**
	 * Stores a Verb in this object's list of Verbs.
	 *
	 * @param v The classname of the verb to load and store.
	 *
	 * @exception ClassNotFoundException if the class 'v' could not be loaded.
	 *
	 * @exception IllegalArgumentException if the class 'v' contains
	 * synonyms for a verb that are already on this object.
	 */
	
	public final void addVerb(String v) throws ClassNotFoundException,
		IllegalArgumentException
	{
		v = Age.intern(v);
		if(verbs == null) verbs=dict();
		internalEnable(v,verbs);
	}
	
	/* all assume d != null */
	
	void internalEnable(String inString, Dictionary d) throws ClassNotFoundException
	{
		String v = Age.intern(inString);
		Verb vb = Age.theUniverse().loadVerb(v);
		
		String vbgcgn = Age.intern(vb.getClass().getName());
		
		Enumeration e = vb.aliases.elements();
		while(e.hasMoreElements())
		{
			if (d.get((String)e.nextElement())!=null)
				throw new IllegalArgumentException ("Sorry, a verb with that synonym/name was already on this object, can't add another!");
		}
		e=vb.aliases.elements();
		while(e.hasMoreElements())
		{
			d.put(Age.intern((String)e.nextElement()),vbgcgn);
		}

	}
	
	void internalDisable(String inString, Dictionary d) throws ClassNotFoundException
	{
		if (d == null) throw new IllegalArgumentException ("There are no verbs on that object.");
		String s=Age.intern(inString);
		Verb v;
		
		v = Age.theUniverse().dynLoadVerb(s);
		
		String vgcgn = Age.intern(v.getClass().getName());
		Enumeration e = v.aliases.elements();
		
		while(e.hasMoreElements())
		{
			Object o = e.nextElement();
			Object nn = d.get(o);
			if (s != nn)
			{
				if (s != nn)
					throw new IllegalArgumentException(s+" != "+nn +": you can't remove that verb!");
			}
			d.remove(o);
		}
	}
	
	void internalVerbList(StringBuffer sb, Dictionary d, String aorf)
	{
		if(d != null)
		{
			Enumeration e = d.elements();
			Hashtable h = new Hashtable();
			while(e.hasMoreElements())
			{
				Object o = e.nextElement();
				if(h.get(o) == null)
				{
					h.put(o,o);
					sb. append("\n\t").
						append(aorf).
						append(" \"").
						append(o).
						append("\"");
				}
			}
		}
	}
	
	/**
	 * Removes a verb from a Thing.
	 *
	 * @param s The classname (twisted.reality.plugin.Take,
	 * divunal.common.magic.Zorch) of the verb to get rid of.
	 */
	
	public final void removeVerb(String s) throws ClassNotFoundException
	{
		internalDisable(s,verbs);
		/* garbage collect unused tables */
		if (verbs.isEmpty())
			verbs=null;
	}
	
	/**
	 * Remove an object from the game entirely, freeing it to be
	 * garbage collected.  Do this when you're done with a Thing, or
	 * when you want it destroyed.
	 */
	
	public void dispose()
	{
		place(null);
		Age.theUniverse().removeSyn(this);
		ref.t=null;
	}
	
	/**
	 * The classname to write when writing to file.
	 */
	
	String typeName()
	{
		if(getClass().getName().equals("twisted.reality.Thing"))
			return "Thing";
		else return getClass().getName();
	}
	
	Dictionary appends;
	
	Enumeration descriptionElements()
	{
		return (appends == null) ? null : appends.elements();
	}
	
	Enumeration descriptionKeys()
	{
		return (appends == null) ? null : appends.keys();
	}
	
	/**
	 * Append a keyed phrase to the description of a Thing.	 This
	 * method allows you to modularize descriptions so they can be
	 * manipulated without re-setting the whole description.
	 *
	 * @param property The name of the key to the property
	 *
	 * @param description The contents of the description component
	 */
	
	public void putDescriptor (String property, String description)
	{
		putDescriptor(property,(Object)description);
	}
	
	/**
	 * Append a keyed, perspective-dependant phrase to the description
	 * of a Thing.  This method allows you to modularize descriptions
	 * so they can be manipulated without re-setting the whole
	 * description.
	 * 
	 */
	public void putDescriptor (String property, Object[] description)
	{
		putDescriptor(property,(Object)description);
	}
	
	/**
	 * A utility function which is equivalent to putDescriptor
	 * (String,Object[]), but converts the Vector to an Object[]
	 * first.
	 */
	
	public void putDescriptor(String property, Vector description)
	{
		putDescriptor(property,fromVector(description));
	}
	
	void putDescriptor(String property, Object description)
	{
		if(appends == null) 
			appends=new twisted.util.LinkedList();
		appends.put(Age.intern(property),description);

		synchronized(myObservable)
		{
			Enumeration e = myObservable.elements();
			while(e.hasMoreElements())
			{
				Player p = (Player) e.nextElement();
				p.notifyDescriptAppend(property,description);
			}
		}
	}
	
		
	/** 
	 * Remove a keyed phrase that has been added to the description
	 * of a Thing.
	 *
	 * @param property The description-element to remove.
	 *
	 * @see putDescriptor 
	 */
	
	public void removeDescriptor(String property)
	{
		if(appends != null)
		{
			if(appends.remove(property) != null)
			{
				synchronized(myObservable)
				{
					Enumeration e = myObservable.elements();
					while(e.hasMoreElements())
					{
						Player p = (Player) e.nextElement();
						p.notifyDescriptRemove(property);
					}
				}
			}
			/* garbage collect unused tables */
			if (appends.isEmpty())
				appends=null;
		}
	}
	
	
	
	/**
	 * The file-persistence body of a Thing.  This is mostly useful
	 * for authors to maintain the map and to make sure "cruft" (extra
	 * properties and things) don't accumulate.
	 * 
	 * @see twisted.reality.author.Scrutinize
	 */
	
	String content()
	{
		StringBuffer r = new StringBuffer();
		
		internalVerbList(r,verbs,"feature");
		
		if(props != null)
		{
			Enumeration e=props.elements();
			Enumeration ee = props.keys();
			while(e.hasMoreElements())
			{
				r.append("\n\t");
				Object q = ee.nextElement();
				Object o = e.nextElement();
				if(o instanceof String || o instanceof Object[])
				{
					r	.append("string \"")
						.append(StringLegalizer.legalize(String.valueOf(q)))
						.append("\" ")
						.append(formatArrayOrString(o));
				}
				else if (o instanceof Integer)
				{
					r.append("int \"").append(StringLegalizer.legalize(String.valueOf(q))).append("\" ").append(StringLegalizer.legalize(String.valueOf(o)));
				}
				else if (o instanceof Long)
				{
					r.append("long \"").append(StringLegalizer.legalize(String.valueOf(q))).append("\" ").append(StringLegalizer.legalize(String.valueOf(o)));	
				}
				else if (o instanceof Float)
				{
					r.append("float \"").append(StringLegalizer.legalize(String.valueOf(q))).append("\" \"").append(StringLegalizer.legalize(String.valueOf(o))).append('\"');
				}
				else if (o instanceof Boolean) 
				{
					r.append("boolean \"").append(StringLegalizer.legalize(String.valueOf(q))).append("\" ").append(StringLegalizer.legalize(String.valueOf(o)));
				}
				else if (o instanceof ThingIdentifier)
				{
					if (((ThingIdentifier) o).sThing()!=null)
						r.append("thing \"").append(StringLegalizer.legalize(String.valueOf(q))).append("\" \"").append((((ThingIdentifier)o).sThing()).NAME()).append('\"');
				}
				else if (o instanceof DynPropWrap)
				{
					r.append("\n\tproperty \"").append(StringLegalizer.legalize(String.valueOf(q))).append("\" \"").append(((DynPropWrap)o).intern).append("\"");
				}
				else if (o instanceof Persistable)
				{
					String cname = o.getClass().getName();
					String pdata = persistableToString((Persistable)o);
					
					r.append("\n\tpersistable \"").append(StringLegalizer.legalize(String.valueOf(q))).append("\" \"").append(cname + "\" ").append(pdata);
				}
			}
		}
		
		if(eventhandlers != null)
		{
			Enumeration e=eventhandlers.elements();
			Enumeration g=eventhandlers.keys();
			while(e.hasMoreElements())
			{
				Object p = g.nextElement();
				Object o = e.nextElement();
				r.append("\n\thandler \"").append(p).append("\" \"").append(o).append("\"");
			}
		}
		
		if( (appends != null) )
		{
			Enumeration e=appends.elements();
			Enumeration g=appends.keys();
			while(e.hasMoreElements())
			{
				Object o = e.nextElement();
				Object p = g.nextElement();
				
				r	.append("\n\tdescript \"")
					.append(p)
					.append("\" ")
					.append(formatArrayOrString(o));
			}
		}
		
		if( (superclass != null) && superclass.sThing() != null)
		{
			r.append("\n\textends \"").append(superclass.sThing().NAME()).append("\"");
		}
		
		if(isComponent())
		{
			r.append("\n\tcomponent");
		}
		
		if (ll != null)
		{
			Enumeration e = names();
			while (e.hasMoreElements())
			{
				r.append("\n\tsyn \"").append(e.nextElement()).append("\"");
			}
		}
		
		return "\tname \"" + StringLegalizer.legalize(NAME())
			+ "\"\n\tdescribe \"" + StringLegalizer.legalize(DESC()) + "\"" 
			+ ( (mood!=null) ? ("\n\tmood \""+ StringLegalizer.legalize (mood())) + "\"": "")
			+ ( (loc!=null) ? ("\n\tplace \"" + StringLegalizer.legalize (loc.NAME()) ) + "\"" : "" )
			+ ( (gender!='n') ? "\n\tgender " + gender : "")
			+ ( (theme!=null) ? ("\n\ttheme \"" + StringLegalizer.legalize(theme)+'\"' ):"")
			+  r;
	}
	
	private String formatArrayOrString(Object o)
	{
		if (o instanceof Object[])
		{
			Object[] ox = (Object[]) o;
			StringBuffer sb = new StringBuffer("{");
			for (int i = 0; i < ox.length;i++)
			{
				sb.append(formatArrayOrString(ox[i]));
				if (i < (ox.length-1))
					sb.append(", ");
			}
			sb.append("}");
			return sb.toString();
		}
		else if (o instanceof String)
		{
			return "\""+StringLegalizer.legalize((String)o)+"\"";
		}
		else if (o instanceof Thing)
		{
			return String.valueOf(Name.of((Thing)o));
		}
		else
		{
			return String.valueOf(o);
		}
	}
	
	private String persistableToString(Persistable p)
	{
		if (Age.theUniverse().PERSISTS != null)
		{
			Object o = Age.theUniverse().PERSISTS.get(p);
			if(o!=null)
			{
				return "key \"" + o + "\"";
			}
			else
			{
				Age.theUniverse().PERSISTS.put(p,p.toString());
			}
		}
		return "val \"" + twisted.util.StringLegalizer.legalize(p.persistance()) + "\" key \"" + p.toString() + "\"";
	}
	
	/**
	 * Returns the file-persistance data of this object.  Please note
	 * that the only items which are stored are:<BR>
	 *
	 * <UL>
	 * <LI>the name
	 * <LI>the description
	 * <LI>all associated Properties that are instances of :
	 * <UL>
	 * <LI>Boolean
	 * <LI>Integer
	 * <LI>String
	 * <LI>Long
	 * <LI>Float
	 * <LI>Thing (or a subclass thereof)
	 * <LI>DynamicProperty
	 * <LI>A Subclass of Persistable
	 * </UL>
	 * </UL>
	 * <br>
	 * 
	 * When subclassing thing, you will find it easiest just to use
	 * the builtin Property API.  It is possible (and not very
	 * difficult) to rewrite the file persistance and loading segments
	 * of the program so that your objects will store and reload
	 * themselves properly, but let me caution against doing this
	 * because your thingclasses/playerclasses/roomclasses etcetera
	 * will lose their portability entirely.
	 *
	 * This method is mostly useful for those authors who want to
	 * debug verbs that they are writing to make sure that there are
	 * no extra properties being created.
	 *
	 * @return the complete string representation of this Thing
	 * 
	 * @see twisted.reality.author.Scrutinize
	 */
	
	public String persistance()
	{
		try 
		{
			return typeName() + "\n{\n" + content() + "\n}\n";
		}
		catch (RuntimeException e)
		{
			e.printStackTrace();
			Age.log(name() + " caused an error in file output.");
		}
		return "";
	}
	
	/**
	 * Returns the name of this object.	 This is so as to be forgiving
	 * to people who forget to write verbs properly. (I.E. if you
	 * forget to indicate you mean blah.name() and you say "Bob
	 * scrunches the " + blah + ".", you will still get the correct
	 * result.	Please don't take advantage of this though, it's bad form.
	 */
	
	public String toString()
	{
		return name();
	}
	
	/**
	 * Adds a synonym for this object.
	 *
	 * @param s The synonym to add.
	 */
	
	public final void addSyn(String s)
	{
		if (!NAME().toLowerCase().equals(s.toLowerCase()) && ll.get(s)==null)
		{
			ll.addElement( Age.intern(s.toLowerCase()) );
			if(loc!=null)
			{
				loc.singlesyn(s,this);
				if ((loc.isBroadcast()) && (loc.place()!=null))
					loc.place().singlesyn(s,this);
			}
		}
	}
	
	/**
	 * Removes a synonym for this object.
	 *
	 * @param s The synonym to remove.
	 */
	
	public final void removeSyn(String s)
	{
		String stlc = s.toLowerCase();
		if(ll.get(stlc)!=null)
		{
			ll.remove(stlc);
			if(loc!=null)
			{
				loc.removesingle(stlc,this);
				if ((loc.isBroadcast()) && loc.place() != null)
					loc.place().removesingle(s,this);
			}
		}
	}
	
	/**
	 * Returns an enumeration of Strings, which represents the list of
	 * synonyms for this object.
	 */
	
	public final Enumeration names()
	{
		return ll.elements();
	}
	
	/**
	 * This hashtable stores all verbs associated with this object.
	 */
	
	private Dictionary verbs;
	
	/**
	 * This hashtable stores all event handlers that this object can
	 * recognize.
	 */
	
	private Dictionary eventhandlers;
	
	/**
	 * This LinkedList stores all the synonyms on this object.
	 */
	
	twisted.util.LinkedList ll;
	
	/**
	 * Set whether or not this object is a component.  If it is, the
	 * object is immoveable and not present in the object list.  You
	 * will want to make things like rugs, safes, walls, windows, etc,
	 * components, because they're really just features of the room in
	 * which they reside. Don't call this function often - there's no
	 * good reason to switch something's state from component to
	 * not-component back and forth a lot.
	 *
	 * @param yn The component-state of this object.
	 */
	
	public void setComponent(boolean yn)
	{
		if (comp == yn) return;
		
		comp=yn;

		if(loc!=null)
		{
			loc.updateNameFor(this);
			Portal shortcut;
			if (!comp 
				&& (loc instanceof Room)
				&& (shortcut=((Room)loc).getPortalByThing(this))
				!=null)
			{
				shortcut.setThing(null);
			}
		}
	}
	
	/**
	 * This boolean indicates whether or not the object is a component
	 * in the scene that it is present in.	If it is a component, the
	 * object is immovable, and does not show up in the item listing
	 * of the room.
	 * 
	 * @return true is this thing is a component, false otherwise.
	 */
	
	public boolean isComponent()
	{
		return comp;
	}
	boolean comp;
	
	/**
	 * This sets the superclass of this object, the class which it is
	 * derived from. As in Java, Things may have only one superclass.
	 *
	 * @param t the new superclass
	 */
	
	public final boolean setSuperClass(Thing th)
	{
		ThingIdentifier t = null;
		if(th != null) t = th.identifier();
		superclass = t;
		if(th!=null)
		{
			Thing someTempThing = this;
			while( someTempThing != null )
			{
				someTempThing = (someTempThing.superclass != null) ? someTempThing.superclass.sThing() : null;
				if(someTempThing == this)
				{
					superclass = null;
					
					Age.log("Warning!  You used a circular dependency!	I was loading " + this.name() + ", and it might not work, but this is your fault!");
					
					return false;
				}
			}
		}
		return true;
	}
	
	/**
	 * This stores a link to the superclass of this object.
	 */
	
	ThingIdentifier superclass;
	
	/**
	 * Maintains a record of the Thing's location.
	 */
	
	protected Location loc;


	// this used to be noun
	/**
	 * Change the description of the specified nameable to a new one.
	 *
	 * @param x The new description
	 */
	
	void idescribe(String x)
	{
		myDesc = (x!=null) ? Age.intern(x):null;
	}
	
	/**
	 * Returns the description of this describable object.
	 */ 
	
	public String describe()
	{
		return myDesc;
	}
	
	/**
	 * Returns the unmodified description of this object.  This method
	 * is only useful in a few esoteric cases related to dynamic
	 * properties.
	 * 
	 * @see twisted.reality.DynamicProperty
	 */ 
	
	public final String DESC()
	{
		return myDesc;
	}
	
	/**
	 * Create a new Noun with the specified name and description.
	 * 
	 * @param nm The name
	 * @param ds The description
	 */ 
	
	Thing(String nm,String ds)
	{
		super(nm);
		if(ds != null)
			describe(ds);
	}
	String myDesc;
}
