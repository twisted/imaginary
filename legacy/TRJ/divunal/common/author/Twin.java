package divunal.common.author;
import twisted.reality.*;

public class Twin extends Verb
{
	public Twin()
	{
		super("twin");
		alias("untwin");
	}
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Location l = d.place();
		
		if (d.verbString().equals("twin"))
		{
			if (p.getBool("twinned"))
			{
				p.hears("You should untwin first, or you won't be able to turn back!");
				return true;
			}
			String twinDesc = p.getString("twin description");
			if (twinDesc == null)
			{
				twinDesc = " flickers for a moment, and assumes the form of ";
			}
			Thing target = d.directObject();
			String tname = target.name();
			Object[] ptSees = {"You adopt the form of ",target};
			Object[] otSees = {p.getString("name"), twinDesc, target};
			l.tellAll(p, ptSees, otSees);
			p.putString("description", target.describe());
			if (p.getString("name") != null)
				p.putString("old apparent name", p.getString("name"));
			p.putString("old name", p.NAME());
			p.putString("name", tname);
			p.name("other "+tname);
			p.addSyn(tname);
			p.putBool("twinned", true);
		}
		else
		{
			if (p.getBool("twinned") != true)
			{
				p.hears("You aren't twinned right now... Are you?");
				return true;
			}

			String fakeName = p.name();
			p.name(p.getString("old name"));
			p.removeProp("old name");
			p.removeProp("description");
			p.removeSyn(p.getString("name"));
			p.removeProp("name");
			if (p.getString("old apparent name") != null)
				p.putString("name", p.getString("old apparent name"));
			p.removeProp("old apparent name");
			p.removeProp("twinned");

			String untwinDesc = p.getString("untwin description");
			if (untwinDesc == null)
			{
				untwinDesc = "'s image flickers and fades away, revealing ";
			}
			Object[] puSees = {"You revert to your original form."};
			Object[] ouSees = {fakeName, untwinDesc, p.name()};
			l.tellAll(p, puSees, ouSees);
		}
		return true;
	}
}
