package divunal.tenth;
import twisted.reality.*;

public class LibraryDoorOpen extends Verb
{
	public LibraryDoorOpen()
	{
		super ("open");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		if (d.directObject().place() == d.place())
		{
			return false;
		}
		else
		{
			Object[] futile = {d.subject(), " gropes for a handhold on the door, and spends a few seconds tugging inneffectually on one of the pistons before finally giving up."};
			Object[] silly = {"After some experimentation, you discover that the door is large, heavy, and has no usable handholds, and that standing around tugging inneffectually on the pistons makes you look silly."};
			d.place().tellAll(d.subject(),silly,futile);
			return true;
		}
	}
}
