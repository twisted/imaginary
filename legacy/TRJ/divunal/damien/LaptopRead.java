package divunal.damien;
import twisted.reality.*;

public class LaptopRead extends Verb
{

	public LaptopRead()
	{
		super("read");
		alias ("look");
	}

	public boolean action(Sentence d) throws RPException
	{
		Player player = d.subject();
		Thing thing = d.directObject();
		Location room = d.place();

		Object[] whatOthersHear = {player, " glances casually at ", thing, "."};
		Object[] whatPlayerHears = {"You glance casually at ",thing,"."};
		room.tellAll(player,whatPlayerHears,whatOthersHear);
		return true;
	}
}






























