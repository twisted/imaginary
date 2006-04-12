
package twisted.reality.author;

import twisted.reality.*;

import java.util.Enumeration;
import java.util.Vector;

public class ClusterBomb extends Verb
{
	public ClusterBomb()
	{
		super("cluster");
	}
	
	public static Enumeration traverse(Room r)
	{
		Vector v = new Vector();
		traverse(v,r);
		return v.elements();
	}
	
	static void traverse(Vector v, Room r)
	{
		if (v.contains(r)) return;

		v.addElement(r);
		Enumeration e = r.allPortals();
		while (e.hasMoreElements())
		{
			Portal p = (Portal) e.nextElement();
			if (p.sThing()!=null) continue;
			traverse(v,p.sRoom());
		}
	}

	public boolean action(Sentence d)
	{
		if (d.place() instanceof Room)
		{
			Enumeration e = traverse((Room)d.place());
			while(e.hasMoreElements())
			{
				d.subject().hears( ((Thing)e.nextElement()).name() );
			}
		}
		return true;
	}
}
