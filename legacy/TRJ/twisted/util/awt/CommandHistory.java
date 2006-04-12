package twisted.util.awt;

public class CommandHistory
{
	CommandHistory(String s)
	{
		command=s;
	}
	
	CommandHistory(String s, CommandHistory p)
	{
		p.next=this;
		prev=p;
		command=s;
	}
	CommandHistory next;
	String command;
	CommandHistory prev;
}
