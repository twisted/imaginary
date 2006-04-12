package divunal.common.author;

import twisted.reality.*;

public class Listen extends Verb
{
	public Listen()
	{
		super("listen");
		alias("unlisten");
	}

	public boolean action(Sentence d) throws RPException
	{
		if (!d.subject().isGod()) return false;

		Player p = d.subject();
		String handled = p.getHandler("say");

		if (d.verbString().equals("listen"))
		{
			if (!(handled.equals("divunal.common.author.SpeechNotify")))
			{
				try
				{
					p.putHandler("say", "divunal.common.author.SpeechNotify");
					p.hears("Listening...");
				}
				catch (ClassNotFoundException cnfe)
				{
					p.hears("um... not so much.");
				}
			}
			else
			{
				p.hears("You're already Listening.");
			}
		}
		else if (handled.equals("divunal.common.author.SpeechNotify"))
		{
			p.removeHandler("say");
			p.hears("No longer Listening.");
		}
		else
		{
				p.hears("You weren't Listening anyway.");
		}

		return true;
	}
}
