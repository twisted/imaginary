package twisted.reality;

class DynPropWrap extends DynamicProperty
{
	String intern;
	public DynPropWrap(String s) throws ClassNotFoundException
	{
		intern=Age.intern(s);
		Age.theUniverse().dynLoadProp(s);
	}
	
	public Object value(Thing origin, Thing destination)
	{
		try
		{
			return Age.theUniverse().dynLoadProp(intern).value(origin,destination);
		} catch (ClassNotFoundException e) {
			Age.log("Error using dynamic property: " + e);
			return null;
		}
	}
}
