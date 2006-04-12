package twisted.reality;
import java.util.Enumeration;
import twisted.util.EnumerationFactory;
/**
 * This exception gets thrown when a player might be referring to more
 * than one object in their current context.  Its string format will
 * prompt the player to be more specific and give them a choice of all
 * the objects that they might be referring to.
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class AmbiguousException extends RPException
{
	public AmbiguousException(Enumeration a, String str, Thing obsrv) 
	{
		ar=new EnumerationFactory(a);
		s=str;
		mt=obsrv;
		/*printStackTrace();*/
	}
	Thing mt;
	public String toString()
	{
		StringBuffer r=new StringBuffer("When you say ").append(s).append(", do you mean ");
		
		Enumeration e = ar.elements();
		while(e.hasMoreElements())
		{
			Thing t = (Thing) e.nextElement();
			if(e.hasMoreElements())
				r.append(t.the()).append(t.nameTo(mt)).append(", ");
			else
				r.append("or ").append(t.the()).append(t.nameTo(mt)).append("?");
		}
		return r.toString();
	}
	public Enumeration elements()
	{
		return ar.elements();
	}
	String s;
	EnumerationFactory ar;
}
