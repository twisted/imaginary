package divunal.common.skills;

import twisted.reality.*;
import divunal.Divunal;

public class MindSpeak extends divunal.common.Skill
{
    public MindSpeak()
    {
		super("mindspeak");
		alias("mindsay");
		alias("mindwhisper");
    }

	public float dailyIncrement() {return 0.05f;}
	public String relevantStat() {return "psyche";}
	public String skillName() {return "mindspeak";}

	public boolean learnSkill(Player p)
	{
		String sname = skillName();

		// If the player's base psyche sucks,
		// They can't learn this ability.

		if (p.getFloat("psyche") < 0)
		{
			p.hears("You just can't seem to understand the idea...");
			return false;
		}

		if (p.getFloat(sname) != 0)  // You can't learn it twice. :)
		{
			p.hears("You've already learned that technique.");
			return false;
		}

		// Since you're learning it, be sure to make it not be zero anymore.
		p.putFloat(sname, 0.1f);
		return true;
	}

    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		Room r = (Room) d.place();
		Thing target = Age.theUniverse().findThing(d.indirectString("to"));
		String mindSpeech = d.directString();
		String verbName = d.verbString();
		boolean isPlayer = (target instanceof Player);
		Player targetp;
		
		if (p.getFloat(verbName) == 0)
			throw new NoSuchVerbException(verbName);
		
		if (isPlayer)  // if the target is a player, good.
			targetp = (Player) target;
		else          // if not, let them know and quit.
		{
			Object[] ydt = {"You don't think that ",
							target,
							" would be able to hear your call."};			
			p.hears(ydt);
			return true;
		}

		// Both the player and target's psyche's are taken into account
		// in the process of sending and recieving the message.

		// If the target isn't logged in, they are informed that their
		// attempt has failed.

		if(targetp.place() == null)
		{
			Object[] phr={"You reach out for ",targetp," with your mind, but you can't seem to reach ",Pronoun.of(targetp),"..."};
			p.hears(phr);
			return true;
		}
		
		// Compare both the Player's current calculated MindSpeak skill,
		// and the reciever's psyche.

		float result = getCurrentSkill(p);

		result += Divunal.statGetCurrent(targetp, "psyche");
		result += Divunal.makeModifier();

		// If the player did a good job, they know it worked... If they
		// didn't, they might not know.

		Object[] targetHears = null;
		Object[] playerResult = null;
		Object[] pTries = null;

		//Records that the Player has successfully used this skill, so that
		//their skill will improve at the end of the day.
		updateSkill(p);  

		if (random() > 0.5)
			{Object[] pT = {"You close your eyes, and call out to ",targetp," with your mind..."}; pTries = pT;}
		else 
			{Object[] pT = {"You reach out to ",targetp," with your mind..."}; pTries = pT;}

		if (result > 0.3)
		{
			// If Player did a really good job, the target gets a clear
			// message, and can identify the voice. If Player was
			// "whispering", the reciever still won't know who sent it, no
			// matter how good the mental connection is.

			if(d.verbString().equals("mindwhisper"))
			{Object[] tH = {random(mindSpeakStart),mindSpeech,"\"."}; targetHears = tH;}
			else
			{Object[] tH = {p,random(mindSpeakGoodStart),mindSpeech,"\"."}; targetHears = tH;}

			{Object[] pR = {"... And your thoughts touch for a moment."}; playerResult = pR;}
		}
		else if (result > 0)
		{
			// If the Player just barely succeeded or failed, they won't be
			// able to tell if they were successful. The recipient also won't
			// be able to tell who sent the call.

			{Object[] tH = {random(mindSpeakStart), mindSpeech,"\"."}; targetHears = tH;}
		}
		else if (result > -0.3)
		{
			// If they almost succeeded, the target still notices the
			// attempt at communication.
			{Object[] tH= {random(mindSpeakFailure)}; targetHears = tH;}
		}
		else
		{
			// The player just plain flopped on this one, and they know it.
			{Object[] pR = {"You close your eyes in concentration, but just can't manage to focus."}; playerResult = pR;}
		}

		Object[] othersSee = {p," closes ", Name.of("eyes",p), random(mindSpeakAttempt)};

		// Let the player know what's up

		r.tellAll(p, pTries, othersSee);
		
		// Delay them while they work...

		p.delay(5);

		// Tell the target and/or player of the results, if applicable

		if (targetHears != null)
			targetp.hears(targetHears);
		else if (playerResult != null)
			p.hears(playerResult);

		// Knock out the player if this tires them out too much...

		if (Divunal.majorStun(p, 0.1f, r) < -1)
			p.hears("Your head throbs from the effort, and the world begins to fade to darkness as you collapse to the ground...");

		return true;
	}

	public static final String[] mindSpeakFailure =
	{
		"You get an odd tinging feeling in the back of your head...",
		"You hear a faint noise, like distant whispering...",
		"There is a faint, echoing voice in the back of your head, but it quickly fades into silence.",
		"A distant voice echoes in your mind, and then falls silent."
	};

	public static final String[] mindSpeakStart =
	{
		"A faint sound in the back of your mind resolves itself into words... \"",
		"A voice echos through your mind... \"",
		"A string of words begins to appear in your mind... \"",
		"Words begin to form in your mind... \""
	};
	
	public static final String[] mindSpeakGoodStart =
	{
		"'s voice echos in your mind... \"",
		"'s thoughts float through your mind... \"",
		"'s mind touches yours for a moment... \"",
		"'s mental voice says, \"",
		"'s mind speaks to yours... \""
	};

	public static final String[] mindSpeakAttempt =
	{
		" for a moment.",
		" in concentration.",
		".",
		" and seems very distant for a moment.",
		" briefly."
	};
}
