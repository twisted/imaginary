package divunal.common.author;
import twisted.reality.*;
import divunal.Divunal;

public class TweakRandom extends Verb
{
	public TweakRandom()
	{
		super("tweakrandom");
		alias("snap");
	}

	public boolean action(Sentence d) throws RPException
	{
		Player p = d.subject();
		Location l = d.place();
		float f = Divunal.makeModifier();
		String descriptor =  "and a faintly glowing \""+f+"\" rune appears in the air for a moment.";

		Object[] otherhear = {p," snaps ",Name.of("fingers",p),", ",descriptor};
		Object[] uhear = {"You snap your fingers, ",descriptor};
		
		l.tellAll(p,uhear,otherhear);
		
		return true;
	}
}
