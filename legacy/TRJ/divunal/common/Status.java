package divunal.common;

import twisted.reality.*;
import divunal.Divunal;

public class Status extends Verb
{

	public Status()
	{
		super("status");
		alias("diagnose");
	}

	public static final String Dying[] =
	{
		"severely wounded, and can feel the cold hand of death upon you...",
		"mortally wounded, and dangerously close to death...",
		"gravely wounded, and hanging onto your life by a thread...",
		"fatally wounded, and perilously close the end of your life..."
	};
	public static final String Wounded[] =
	{
		"badly injured, and in a great deal of pain.",
		"seriously wounded, and barely able to move.",
		"seriously and quite painfully injured.",
		"severely injured, and struggling to stay conscious."
	};
	public static final String Injured[] =
	{
		"seriously injured, ",
		"badly wounded, ",
		"badly hurt, "
	};
	public static final String Hurt[] =
	{
		"bruised and battered, ",
		"in pain, ",
		"hurt, ",
		"mildly injured, "
	};
	public static final String Exhausted[] =
	{
		"totally exhausted.",
		"about to collapse from exhaustion.",
		"totally worn out.",
		"completely exhausted.",
		"close to passing out from exhaustion."
	};
	public static final String Tired[] =
	{
		"extremely tired.",
		"feeling worn out.",
		"feeling extremely tired.",
		"feeling exhausted.",
		"worn out."
	};
	public static final String Winded[] =
	{
		"feeling a bit tired.",
		"feeling winded.",
		"feeling tired.",
		"tired."

	};
	public static final String Fine[] =
	{
		"feeling fine.",
		"feeling okay.",
		"feeling fine.",
		"doing well.",
		"okay.",
	};

    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		float phealth = Divunal.health(p);
		float pstamina = Divunal.percentStamina(p);
		StringBuffer s = new StringBuffer("You");

		if (randomf() > 0.5)
			s.append(" are ");
		else
			s.append("'re ");

		if (phealth < -0.25)
			s.append(random(Dying));
		else if (phealth < -0.50)
			s.append(random(Wounded));
		else if (phealth < 0)
		{
			s.append(random(Injured)).append("and ");
			if (pstamina < 0.25)
				s.append(random(Exhausted));
			else s.append(random(Tired));
		}
		else if (phealth < 0.75)
		{
			s.append(random(Hurt)).append("and ");
			if (pstamina < 0.25)
				s.append(random(Exhausted));
			else if (pstamina < 0.50)
				s.append(random(Tired));				
			else s.append(random(Winded));
		}
		else
		{
			if (pstamina < 0.25)
				s.append(random(Exhausted));
			else if (pstamina < 0.50)
				s.append(random(Tired));
			else if (pstamina < 0.75)
				s.append(random(Winded));				
			else s.append(random(Fine));
		}
		
		p.hears(s.toString());

		return true;
	}
}
