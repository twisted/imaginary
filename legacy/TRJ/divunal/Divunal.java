package divunal;

import twisted.reality.*;
import java.util.Random;

/**
 * This is the base statistics library for the game "Divunal".  Each
 * method is a "stat test".  For instance, calling
 * Divunal.psycheCheck(bob); is the same as "rolling bob's psyche" in a
 * tabletop RPG. 
 * 
 */

public final class Divunal
{
	static Random r = new Random();
	public static final long OneDayMillis = 86400000;
	public static final long MagicHealingTime = 600000;

	public static float makeModifier()
	{
		double rand = r.nextDouble();
		float modifier = (float) 

			// Okay kiddies, this is the GNUPLOT expression used to
			// obtain the really funky-ass randomization routine.
			// hemhem.
			//
			// plot [0:1] [0:1] (-( (log( (x + 0.01) * 100 ) ) / log(10))+2)/2
			//
			// For all you english speaking types, this returns a number
			// between -1 and +1, but much distributed in such a way that
			// numbers at or close to 0 are more common, and numbers
			// approaching 1 are much less likely.

			(
			 (
			  -( 
				(Math.log( (rand + 0.01) * 100 ) )
				/Math.log(10)
				)
			  +2)
			 /2
			 );

		if( r.nextDouble() > .5 )
		{
			modifier = modifier * (-1);
		}
		return modifier;
	}

	// Returns the Player X's current Attribute Y value, with experience included.

	public static float statGetCurrent(Player x, String y)
	{
		float myStat = x.getFloat(y);
		myStat += x.getFloat("mojo");
		return myStat;
	}

	// Performs an average challenge of Player X's Y stat, and returns true if the check passed.

	static boolean statCheck(Player x, String y)
	{
		float myStat = statGetCurrent(x,y);
		if (myStat > makeModifier())
			return true;
		return false;
	}

	// weightedStatCheck performs a statistics check of the Player's 
	// requested stat from a base other than zero, and returns the difference. 
	//
	// For example, weightedStrengthCheck(Bob, 0.5) would be based
	// on the comparatively high value of 0.5 rather than the average of 0.
	// A positive number would indicate the degree of Bob's success, and a
	// negative number would indicate the extent of his failure.

	static float weightedStatCheck(Player x, String y, float d)
	{
		float myStat = statGetCurrent(x,y);
		return myStat - (makeModifier()+d);
	}
	
	public static float weightedPsycheCheck(Player x, float d)
	{
		return weightedStatCheck(x,"psyche",d);
	}

	public static float weightedAgilityCheck(Player x, float d)
	{
		return weightedStatCheck(x,"agility",d);
	}

	public static float weightedEnduranceCheck(Player x, float d)
	{
		return weightedStatCheck(x,"endurance",d);
	}

	public static float weightedMemoryCheck(Player x, float d)
	{
		return weightedStatCheck(x,"memory",d);
	}

	public static float weightedDexterityCheck(Player x, float d)
	{
		return weightedStatCheck(x,"dexterity",d);
	}

	public static float weightedStrengthCheck(Player x, float d)
	{
		return weightedStatCheck(x,"strength",d);
	}

	// Does a weighted Psyche check based on the total of the two 
	// players involved, for cooperative efforts like Mind Speak and
	// Mental Chorus.

	public static float combinedPsycheCheck(Player x, Player y, float d)
	{
		float myStat = statGetCurrent(x, "psyche");
		myStat += statGetCurrent(y, "psyche");
		myStat -= (makeModifier()+d);
		return myStat;
	}

	// Opposed Stat Checks
	//
	// Perfoms a slightly randomized check between the opposed stats of Players
	// X and Y. The returned float is from the perspective of player X, with
	// negative floats being the degree of failure, and positive floats being
	// the degree of success.

	public static float opposedStrengthCheck(Player x, Player y, float xM, float yM)
	{
		float myStat = statGetCurrent(x, "strength") + xM;
		myStat -= statGetCurrent(y, "strength") + yM;
		myStat += makeModifier();
		return myStat;
	}

	public static float opposedPsycheCheck(Player x, Player y)
	{
		float myStat = statGetCurrent(x, "psyche");
		myStat -= statGetCurrent(y, "psyche");
		myStat += makeModifier();
		return myStat;
	}

	public static float opposedAgilityCheck(Player x, Player y)
	{
		float myStat = statGetCurrent(x, "agility");
		myStat -= statGetCurrent(y, "agility");
		myStat += makeModifier();
		return myStat;
	}

	public static float opposedDexterityCheck(Player x, Player y)
	{
		float myStat = statGetCurrent(x, "dexterity");
		myStat -= statGetCurrent(y, "dexterity");
		myStat += makeModifier();
		return myStat;
	}

	public static float opposedEnduranceCheck(Player x, Player y)
	{
		float myStat = statGetCurrent(x, "endurance");
		myStat -= statGetCurrent(y, "endurance");
		myStat += makeModifier();
		return myStat;
	}

	public static float opposedMemoryCheck(Player x, Player y)
	{
		float myStat = statGetCurrent(x, "memory");
		myStat -= statGetCurrent(y, "memory");
		myStat += makeModifier();
		return myStat;
	}
	
	// The following methods return the Current stat of the Player,
	// including their Mojo (experience, divine favor, coolness, etc.)
	//
	// psyche(Bob) would return Bob's psyche, as improved by experience.

	public static float psyche(Player x)
	{
		return statGetCurrent(x,"psyche");
	}
	
	public static float agility(Player x)
	{
		return statGetCurrent(x,"agility");
	}
	
	public static float strength(Player x)
	{
		return statGetCurrent(x,"strength");
	}
	
	public static float endurance(Player x)
	{
		return statGetCurrent(x,"endurance");
	}
	
	public static float memory(Player x)
	{
		return statGetCurrent(x,"memory");
	}
	
	public static float dexterity(Player x)
	{
		return statGetCurrent(x,"dexterity");
	}

	// The following methods run an average stat check, and return a
	// boolean pass/fail result. statCheck(Bob, "strength") would return
	// true or false regarding Bob's attempt at an average strength check.

	public static boolean psycheCheck(Player x)
	{
		return statCheck(x,"psyche");
	}
	
	public static boolean agilityCheck(Player x)
	{
		return statCheck(x,"agility");
	}
	
	public static boolean strengthCheck(Player x)
	{
		return statCheck(x,"strength");
	}
	
	public static boolean enduranceCheck(Player x)
	{
		return statCheck(x,"endurance");
	}
	
	public static boolean memoryCheck(Player x)
	{
		return statCheck(x,"memory");
	}
	
	public static boolean dexterityCheck(Player x)
	{
		return statCheck(x,"dexterity");
	}

	// Returns your current health, with regeneration and stuff taken
	// into account.

	public static float health(Player x)
	{
		float newHealth;
		float oldHealth = x.getFloat("health");
		long oldTime = x.getLong("health time");
		long currentTime = System.currentTimeMillis();
		float healingFactor = x.getFloat("healing factor");
		long healTime;

		healTime = (long) (OneDayMillis * (healingFactor + 1));
			
		newHealth = (float) ((currentTime - oldTime) / (float) healTime);

		newHealth += oldHealth;

		if (newHealth > 1)   // cap health at 1.0, the normal human max
			newHealth = 1;   // (everyone is equally structurally sound)

		x.putFloat("health", newHealth);
		x.putLong("health time", currentTime);

		return newHealth;

        /* In short, whenever you call health(player), it updates the 
		   player's current health with whatever they would have recovered
		   over time since the last check.
		   
		   BTW: Players will normally regenerate their health (up to 1.0)
		   in 24 hours (864 x 10^5 Milliseconds). This rate is also governed
		   by the Player's Healing Factor. A healing factor of 0
		   has no effect, 0.5 will double recovery speed, -0.5 will
		   halve it, etc.
		*/
	}

	// Return a float between 0 and 1 representing your current percentage
	// of total health.

	public static float percentHealth(Player x)
	{
		return (health(x) + 1) / (2); 
	}

	// Returns your current Stamina, with regeneration and stuff taken
	// into account.
	
	public static float stamina(Player x)
	{
		float newStamina;
		float oldStamina = x.getFloat("stamina")+1; //adding one (1 to 2 scale)
		long oldTime = x.getLong("stamina time");
		float maxStamina = endurance(x)+1;          //adding one (1 to 2 scale)
		long currentTime = System.currentTimeMillis();
		float currentHealth = health(x)+1;          //adding one (1 to 2 scale)
		float hFactor = currentHealth / 1;
		float healingFactor = x.getFloat("healing factor");
		long healTime;

		healTime = (long) (MagicHealingTime * (healingFactor + 1));

		newStamina = (float) ((currentTime - oldTime) / (float) healTime);

		newStamina += oldStamina;

		if (newStamina > maxStamina)
			newStamina = maxStamina;
		if ((newStamina / maxStamina) > hFactor)
			newStamina = maxStamina * hFactor;

		newStamina -= 1;  // Put stamina back to a -1 to +1 scale

		x.putFloat("stamina", newStamina);
		x.putLong("stamina time", currentTime);

		return newStamina;

		/* In short, whenever you call stamina(player), it updates the 
		   player's current stamina with whatever they would have recovered
		   over time since the last check. Stamina is capped at the player's
		   max stamina (their endurance, which runs from -1 to 1), and also
		   cannot be proportionately higher than their current health.
		   
		   BTW: Players will normally regenerate their stamina completely in
		   10 minutes (864 x 10^5 Milliseconds). A healing factor of 0 has 
		   no effect, 0.5 will double recovery speed, 1.5 will halve it, etc.
		*/
	}

	// Return a float between 0 and 1 representing your current percentage
	// of total Stamina.

	public static float percentStamina(Player x)
	{
		return (stamina(x) + 1) / (x.getFloat("endurance") + 1); 
	}

	public static void knockOut(Player p, int time)
	{
		Object[] outDescriptor = {Name.of(p), " is in a slumped, lifeless position, apparently unconcious."};
		p.mood("unconcious");
		p.putDescriptor("unconcious", outDescriptor);
		if (time < 30)
		{
			p.hears("(You have been stunned for "+time+" seconds.)");
			p.delay(time);
		}
		else
		{
			p.hears("(You have been knocked unconcious...)");
			p.hears("(You will recover in "+time+" seconds...");
			p.delay(time);
		}
		p.removeDescriptor("unconcious");
		p.mood(null);
	}

	public static void knockOut(Player p, int time, Room here)
	{
		Object[] outDescriptor = {Name.of(p), " is in a slumped, lifeless position, apparently unconcious."};
		Object[] fallDown = {p, " collapses, unconcious."};
		Object[] getUp = {p, " begins to sit up, looking somewhat recovered."};
		here.tellAll(p, null, fallDown);
		p.mood("unconcious");
		p.putDescriptor("unconcious", outDescriptor);
		if (time < 30)
		{
			p.hears("(You have been stunned for "+time+" seconds.)");
			p.delay(time);
		}
		else
		{
			p.hears("(You have been knocked unconcious...)");
			p.hears("(You will recover in "+time+" seconds...");
			p.delay(time);
		}
		here.tellAll(p, null, getUp);
		p.removeDescriptor("unconcious");
		p.mood(null);
	}

    // Inflict Stamina damage, but never knock the subject unconcious
    public static float minorStun(Player p, float ammount)
    {
    	float pstamina;
        long ctime = System.currentTimeMillis();

        pstamina = stamina(p);
        ammount = ammount * (1 - p.getFloat("defense"));
        pstamina -= ammount;

		if (pstamina < -1) pstamina = -1;

        p.putFloat("stamina", pstamina);
        p.putLong("stamina time", ctime);

		return pstamina;
    }

 	// Inflict Stamina damage, with the possibility of being knocked out.
	public static float majorStun(Player p, float ammount)
	{ 
    	float pstamina;
		int downtime;
        long ctime = System.currentTimeMillis();

        pstamina = stamina(p);
        ammount = ammount * (1 - p.getFloat("defense"));
        pstamina -= ammount;

		if (pstamina < -1)
		{
			pstamina = (float) (pstamina + 0.9)*-100;
			downtime = (int) pstamina;
			knockOut(p, downtime);
			pstamina = -1;
		}

        p.putFloat("stamina", pstamina);
        p.putLong("stamina time", ctime);

    	return pstamina;
    } 

	public static float majorStun(Player p, float ammount, Room here)
	{ 
    	float pstamina;
		int downtime;
        long ctime = System.currentTimeMillis();

        pstamina = stamina(p);
        ammount = ammount * (1 - p.getFloat("defense"));
        pstamina -= ammount;

		if (pstamina < -1)
		{
			pstamina = (float) (pstamina + 0.9)*-100;
			downtime = (int) pstamina;
			knockOut(p, downtime, here);
			pstamina = -1;
		}

        p.putFloat("stamina", pstamina);
        p.putLong("stamina time", ctime);

    	return pstamina;
    } 

	/*
	// Inflict health damage, but with no possibility of being killed.
	public static float minorWound(Player p, float ammount)
	{

	}

	// Inflict health damage. The target player may be knocked out
	// or killed if the damage is sufficient.
	public static float fatalWound(Player p, float ammount)
	{ 

	} 
	*/
}
