package twisted.reality.author;

import twisted.reality.*;

/**
 * <b>allow [local-player : player] to [Verb-classname : x] </b>
 * 
 * <p>Gives player the ability to use verb x. Note that this becomes an
 * innate ability of player.</p>
 *
 * <b>disallow [local-player : player] from [verb-name : verb] </b>
 *
 * <p>Removes player's ability to use verb. </p>
 *
 * <p>Example: If I type "disallow Bob from swim", Bob will lose his
 * ability to use the swim verb, which would be a very cruel thing to
 * do if he was in deep water at the time.</p>
 *
 * @see twisted.reality.author.Enable
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Allow extends Verb
{
	public Allow()
	{
		super("allow");
		alias("disallow");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		if(!d.subject().isGod()) return false;
		if(d.directObject() instanceof Player)
		{
			Player p = (Player) d.directObject();
			if(d.verbString().equals("allow"))
			{
				String vv = d.indirectString("to");
				try
				{
					p.addAbility(vv);
					d.subject().hears("You successfully gifted "+p.name()+" with the ability "+vv+".");	
				}
				catch (ClassNotFoundException e)
				{
					// If addAbility blows up because that class
					// doesn't exist
					d.subject().hears("Gifting failed: " + e);
				}
				catch (IllegalArgumentException iae)
				{
					// If that verb overlaps with synonyms for another
					// verb.
					d.subject().hears(iae.getMessage());
				}
			}
			
			else
			{
				try
				{
					String vv = d.indirectString("from");
					p.removeAbility(vv);
					d.subject().hears("Disallowed.");
				}
				catch (ClassNotFoundException e)
				{
					// If removeAbility blows up because that class
					// doesn't exist
					d.subject().hears("Gifting failed: " + e);
				}
				catch (IllegalArgumentException iae)
				{
					// If removeAbility blows up because the ability
					// wasn't actually on the player
					d.subject().hears(iae.getMessage());
				}
			}
		}
		else
		{
			d.subject().hears("You can't give an ability to a non-player, dimwit!");
		}
		return true;
	}
}
