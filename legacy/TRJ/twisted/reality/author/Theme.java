package twisted.reality.author;

import twisted.reality.*;

/**
 * Change the theme of some Thing to a new thing.  Themes are a "look
 * and feel" add-on so that the game will look different depending on
 * the circumstances. Current themes are:
 *
 * <ul>
 * <li> sgreen, a weird green look by Bryan
 * <li> default, the white-tile theme that's standard
 * <li> greystone, a dungeon-looking theme
 * <li> weird, the name says it all
 * <li> leaf, a leaf theme for forests
 * <li> water, again, self-explaintory
 * </ul>
 *
 * Usage: <code>&gt; theme <b>&lt;thing&gt;</b> to
 * <b>&lt;themename&gt;</b></code>
 *
 * @version 1.0.0, 12 Jun 1999
 * @author Glyph Lefkowitz
 */

public class Theme extends Verb
{
	public Theme()
	{
		super("theme");
		setDefaultPrep("with");
	}
	
	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		if (!p.isGod()) return false;
		d.directObject().setTheme(d.indirectString("to"));
		Object[] godsees = {"You close your eyes and \"think different\"."};
		Object[] othersees = {p," closes ", twisted.reality.Name.of("eyes",p),", and the world seems to shift around ",Pronoun.obj(p),"..."};
		d.place().tellAll(p, godsees, othersees);

		return true;
	}
}
