package divunal.tenth;

import twisted.reality.*;

public class OldWoodenDoorEnter extends Verb
{
    public OldWoodenDoorEnter()
    {
		super("enter");
		alias("open");
		alias("go");
		alias("walk");
		alias("turn");
		alias("twist");
		/*setDefaultPrep("through");*/
    }
    
    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		String s = d.directString();
		Room room = (Room) d.place();
		Thing door = d.directObject().getThing("target door");
		Room destroom = (Room) door.place();
		
		Object[] sadButTrue = {p, " opens the old wooden door, and vanishes."};
		Object[] trueToo = {"You reach for the knob on the door..."};
		
		room.tellAll(p,trueToo,sadButTrue);
		
		Object[] vanishthrough = {p, " vanishes through the old wooden door."};
		Object[] stepthrough = {p, " steps through the old wooden door."};
		
		p.moveTo(destroom,vanishthrough,stepthrough);
		
		Object[] desttell;
		Object[] selftell;
		
		if (p.isGod())
		{
			Object[] dtl = { "The old wooden door swings open, and ", p," steps through it."};
			Object[] stl = { "You open the old wooden door and step through." };
			desttell = dtl;
			selftell = stl;
		}
		else
		{
			Object[] dltg = {"The old wooden door swings open, and ", p, " staggers through, looking a bit disoriented."};
			Object[] stl = { "As you open the old wooden door, you are gripped by a strange feeling of disorientation, and the world seems to spin around you..." };
			desttell = dltg;
			selftell = stl;
		}
		
		destroom.tellAll(p,selftell,desttell);
		
		return true;
    }
    
}
