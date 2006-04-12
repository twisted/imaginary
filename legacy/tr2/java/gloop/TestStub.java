package gloop;

/**
 * The idea is that files like this would somehow be auto-generated,
 * and somehow hook into the reference process to begin with...? 
 * (methinks the protocol needs some more high-level type specificity) 
 */

import java.util.Vector;
import java.io.IOException;

public class TestStub
{
	Glob g;
	public TestStub(Glob ig)
	{
		g=ig;
	}
	public Vector y() throws IOException
	{
		Object[] obj={};
		Glob m = (Glob) g.get("y");
		return (Vector) m.call(obj);
	}
}
