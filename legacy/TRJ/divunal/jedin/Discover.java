package divunal.jedin; 
import twisted.reality.*;
import twisted.util.StringEnumerator;

public class Discover extends Verb 
{
    public Discover() 
    {
		super("discover"); 
    } 
    
    /* This is so a nice little dialog box appears for entering the default room description*/
    public class DescProcessor implements ResponseProcessor
    {
		String direction, name; //direction in which to build, room name
		int x, y, z; //dimensions of grid
		Player player; //who's doing the building
		Room here; //where the person is
		boolean[] exits = new boolean[3]; //what directions have connections <-> them
		
		public DescProcessor(Player subject, Room this_room, int length, int width, int height, String dir, String nam, boolean[] connections)
		{
			player = subject;
			here = this_room;
			x = length;
			y = width;
			z = height;
			direction = dir;
			name = nam;
			exits = connections;
		}
		
		/* This has the description string*/
		public void gotResponse(String s)
		{
			Portal.between(here,
						   generateRooms(x, y, z, direction, name, s/*description*/, exits),
						   direction);
			player.hears("Why don't you take a look?");
		}
    }
	
    public boolean action(Sentence d) throws RPException 
    {
		/*This "parses" the dimension string.  charAt() returns a character, and the integer value of a number is 48 less than its ASCII value*/
		int x = (int)(d.directString().charAt(0) - 48);
		int y = (int)(d.directString().charAt(2) - 48);
		int z = (int)(d.directString().charAt(4) - 48);
		
		/* The z coordinate can be negative, so make sure that a number and not '-' was passed */
		if (z == -3)  //The ASCII value of '-' is 45, so z will == -3 if it was passed 
			z = -(int)(d.directString().charAt(5) - 48);
		
		String direction = d.indirectString("to");
		Player player = d.subject();
		Room player_loc = (Room)d.place();
		
		/* Check to see whether there are any directions in which the player doesn't want exits made. */
		boolean[] exits= {true, true, true};
		StringEnumerator exceptions = new StringEnumerator(d.indirectString("except"));
		while(exceptions.hasMoreElements())
		{
			String word = (String)exceptions.nextElement();
			/* Get rid of "and"s */
			if (word.equals("and"))
				continue;
			else
				switch(word.charAt(0))
				{
				case 'e': case 'w': exits[0] = false; break;
				case 'n': case 's': exits[1] = false; break;
				case 'u': case 'd': exits[2] = false; break;
				}
		}
		
		
		/* Check for errors.  If there aren't any, proceed with construction */
		if (!checkForErrors(player, player_loc, x, y, z, direction))
        {
			String name = d.withString();
			d.subject().requestResponse
				(
				 new DescProcessor(player, player_loc, x, y, z, direction, name, exits),
				 "Default description of " + name, 
				 ""
				 );
		}
		return true;	
    } 
	
    
    /* Makes sure there are no errors in parameters; returns true if there are, false otherwise */
    public static boolean checkForErrors(Player player, Room player_loc, int x, int y, int z, String direction)
    {
		/* Must have a positive number of rooms */
		if ((x <= 0) || (y <= 0))
		{
			player.hears("You've gotta have a positive number of rooms, genius.");
			return true;
		}
		
		/* Since z denotes the height (either up or down), it must be non-zero */
		else if(z == 0)
		{
			player.hears("We live in a three-dimensional world.  No flat rooms here.");
			return true;
		}
		
		/* Grids with any dimension larger than 9 are not allowed: too many rooms! */
		else if ((x > 9) || (y > 9) || (z > 9) || (z < -9))
		{
			player.hears("You find yourself unable to focus enough power for such a huge task.");
			return true;
		}
		
		/* Can't create grids in a given direction if an exit already exists */
		else if(player_loc.getPortal(direction)!=null)
		{
			player.hears("There is already an exit in that direction.");
			return true;
		}
		
		else return false;
    }
	
    
    /* Makes the grid of rooms, returns the one to connect to player's room */
    public static Room generateRooms(int x, int y, int z, String direction, String name, String desc, boolean[] exits)
    {
		/*Coordinate counter variables--used for indexing the grid*/
		int xprime = 0, yprime = 0, zprime = 0;
		/* Since z can be positive or negative, need to use absolute value for looping and indexing */
		int abs_z = Math.abs(z);
		/*Grid of rooms created*/
		Room[][][] grid = new Room[x][y][abs_z];
		
		/*Make the grid of rooms*/
		int counter = 0;
		while(zprime < abs_z)
		{
			yprime = 0;
			while(yprime < y)
			{
				xprime = 0;
				while(xprime < x)
				{
					
					grid[xprime][yprime][zprime] = new Room(name + " #" + counter,desc);
					/* Set the name the player sees--the one that was entered */
					grid[xprime][yprime][zprime].putString("name", name);
					counter++;
					xprime++;
				}
				
				yprime++;
			}
			zprime++;
		}
		
		/*Generate the exits*/
		zprime = 0;
		while(zprime < abs_z)
		{
			yprime = 0;
			while(yprime < y)
			{
				xprime = 0;
				while(xprime < x)
				{
					/*Exits are made w->e, s->n, and d->u*/
					if ((xprime < (x - 1)) && exits[0])
						Portal.between(grid[xprime][yprime][zprime],
									   grid[xprime+1][yprime][zprime],"east");
					if ((yprime < (y - 1)) && exits[1])
						Portal.between(grid[xprime][yprime][zprime],
									   grid[xprime][yprime+1][zprime],"north");
					if ((zprime < (abs_z - 1)) && exits[2])
						Portal.between(grid[xprime][yprime][zprime],
									   grid[xprime][yprime][zprime+1],"up");
					xprime++;
				}
				yprime++;
			}
			zprime++;
		}	
		
		
		/*If grid built down (z<0), will enter at top, else will enter at bottom*/
		int floor = (z < 0) ? abs_z - 1 : 0;
		//The room connected to player's location
		Room ret_room;
		
		/* Connecting room will be in the middle of one side, with height as determined above */
		switch(direction.charAt(0))
		{
		case 'e': 
			ret_room = grid[0][y/2][floor];
			break;
		case 'w':
			ret_room = grid[x-1][y/2][floor];
			break;
		case 'n':
			ret_room = grid[x/2][0][floor];
			break;
		case 's':
			ret_room = grid[x/2][y-1][floor];
			break;
		case 'u':
			ret_room = grid[x/2][y/2][0];
			break;
		default:
		case 'd':
			ret_room = grid[x/2][y/2][abs_z-1];
			break;
		}
		
		return ret_room;
    }
}
