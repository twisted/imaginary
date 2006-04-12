package divunal.agentmoore;

import twisted.reality.*;

public class TMEPush extends Verb
{
    public TMEPush() 
    {
		super("push");
		alias("press");
    }
    
    public static final int RED=1;
    public static final int ORANGE=2;
    public static final int YELLOW=3;
    public static final int GREEN=4;
    public static final int BLUE=5;
    public static final int PURPLE=6;
    public static final int BROWN=7;
    public static final int BLACK=8;
    public static final int WHITE=9;
    public static final int GREY=0;
    
    public void pushRed(Thing door, Room room)
    {
		Persistable prst = door.getPersistable("buttonspressed");
		if (prst == null) 
	    {
			door.putPersistable("buttonspressed",prst=new Stack());
	    }
		Stack stk = (Stack)prst;
		stk.pushInt(RED);
    }

    public void pushOrange(Thing door, Room room)
    {
		Persistable prst = door.getPersistable("buttonspressed");
		if (prst == null) 
	    {
			door.putPersistable("buttonspressed",prst=new Stack());
	    }
		Stack stk = (Stack)prst;
		stk.pushInt(ORANGE);
    }

    public void pushYellow(Thing door, Room room)
    {
		Persistable prst = door.getPersistable("buttonspressed");
		if (prst == null) 
	    {
			door.putPersistable("buttonspressed",prst=new Stack());
	    }
		Stack stk = (Stack)prst;
		stk.pushInt(YELLOW);
    }

    public void pushGreen(Thing door, Room room)
    {
		Persistable prst = door.getPersistable("buttonspressed");
		if (prst == null) 
	    {
			door.putPersistable("buttonspressed",prst=new Stack());
	    }
		Stack stk = (Stack)prst;
		stk.pushInt(GREEN);
    }

    public void pushBlue(Thing door, Room room)
    {
		Persistable prst = door.getPersistable("buttonspressed");
		if (prst == null) 
	    {
			door.putPersistable("buttonspressed",prst=new Stack());
	    }
		Stack stk = (Stack)prst;
		stk.pushInt(BLUE);
    }

    public void pushPurple(Thing door, Room room)
    {
		Persistable prst = door.getPersistable("buttonspressed");
		if (prst == null) 
	    {
			door.putPersistable("buttonspressed",prst=new Stack());
	    }
		Stack stk = (Stack)prst;
		stk.pushInt(PURPLE);
    }

    public void pushBrown(Thing door, Room room)
    {
		Persistable prst = door.getPersistable("buttonspressed");
		if (prst == null) 
	    {
			door.putPersistable("buttonspressed",prst=new Stack());
	    }
		Stack stk = (Stack)prst;
		stk.pushInt(BROWN);
    }

    public void pushBlack(Thing door, Room room)
    {
		Persistable prst = door.getPersistable("buttonspressed");
		if (prst == null) 
	    {
			door.putPersistable("buttonspressed",prst=new Stack());
	    }
		Stack stk = (Stack)prst;
		stk.pushInt(BLACK);
    }

    public void pushWhite(Thing door, Room room)
    {
		Persistable prst = door.getPersistable("buttonspressed");
		if (prst == null) 
	    {
			door.putPersistable("buttonspressed",prst=new Stack());
	    }
		Stack stk = (Stack)prst;
		stk.pushInt(WHITE);
    }

    public void pushGrey(Thing door, Room room)
    {
		Persistable prst = door.getPersistable("buttonspressed");
		if (prst == null) 
	    {
			door.putPersistable("buttonspressed",prst=new Stack());
	    }
        Stack stk = (Stack)prst;
		int adds = 0;
		int magic = stk.popInt();
		while(stk.hasPop()) {
			if (adds < 2) {
				magic = magic + stk.popInt();
				adds++;
			}
			else {
				magic = magic * stk.popInt();
				adds = 0;
			}
		}
		if(magic == door.getInt("code")) {
			Portal way = room.getPortalByThing(door);
			door.putBool("obstructed",false);
			if(way != null)
			{
				way.setObvious(true);
				Portal yaw = way.backtrack();
				yaw.setObvious(true);
			}
			room.tellEverybody("A small green light on top of the keypad begins to blink.");
			room.putDescriptor("lightstate","A small green light is blinking on top of the keypad.");
			Object[] ta = {Name.Of(door)," swings open allowing you entry."};
			room.tellAll(ta);

			door.handleDelayedEvent(new RealEvent("glass door close",null,null),1);
		
		}  else {
			room.putDescriptor("lightstate","A small red light illuminates on top of the keypad.");
		}
    }
    
    public void pushButton(Thing door, Room room, int colorstat)
    {
		room.putDescriptor("lightstate","A small yellow light is blinking on top of the keypad.");
		switch(colorstat)
	    {
	    case RED:    pushRed(door,room); break;
	    case ORANGE: pushOrange(door,room); break;
	    case YELLOW: pushYellow(door,room); break;
	    case GREEN:  pushGreen(door,room); break;
	    case BLUE:   pushBlue(door,room); break;
	    case PURPLE: pushPurple(door,room); break;
	    case BROWN:  pushBrown(door,room); break;
	    case BLACK:  pushBlack(door,room); break;
	    case WHITE:  pushWhite(door,room); break;
	    case GREY:   pushGrey(door,room); break;
	    }
	
    }
    
    public boolean action(Sentence d) throws RPException
    {
		Player p = d.subject();
		String s = d.directString();
		Thing b = d.directObject(); 
		Room room = (Room) d.place();
		Thing door = b.getThing("obstacle");

		int colorstat = -1;
		String buttoncolor = "eh?";

		if      (s.startsWith("red"))    {colorstat = 1; buttoncolor="red";}
		else if (s.startsWith("orange")) {colorstat = 2; buttoncolor="orange";}
		else if (s.startsWith("yellow")) {colorstat = 3; buttoncolor="yellow";}
		else if (s.startsWith("green"))  {colorstat = 4; buttoncolor="green";}
		else if (s.startsWith("blue"))   {colorstat = 5; buttoncolor="blue";}
		else if (s.startsWith("purple")) {colorstat = 6; buttoncolor="purple";}
		else if (s.startsWith("brown"))  {colorstat = 7; buttoncolor="brown";}
		else if (s.startsWith("black"))  {colorstat = 8; buttoncolor="black";}
		else if (s.startsWith("white"))  {colorstat = 9; buttoncolor="white";}
		else if (s.startsWith("grey"))   {colorstat = 0; buttoncolor="grey";}

		if (colorstat != -1)
	    {
			room.tellEverybodyBut(p,p.name() + " pushes the " + buttoncolor + " button.");
			p.hears("You push the " + buttoncolor + " button.");
	    }
		else
	    {
			p.hears("What button do you want to push?");
	    }

	    pushButton(door,room,colorstat);

	    return true;
    }
}
