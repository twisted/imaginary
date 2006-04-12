package twisted.reality.client;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

import java.util.Vector;
import java.util.Enumeration;

public class SystemNozzle implements Nozzle, Runnable
{
	public void completeAction()
	{
		System.out.print("> ");
		System.out.flush();
	}
	public void handleError(Throwable t)
	{
		t.printStackTrace();
	}
	
	public void requestResponse(String ID, String prompt, String deftext)
	{
		System.out.println("response requested: "+ID+" "+prompt+" "+deftext);
	}
	
	public void setTheme(String theme)
	{
		System.out.println("[ Theme: "+theme+" ]");
	}
	
	public void dialog(String string)
	{
		System.out.println("{ "+string+" }");
	}
	
	public void logout()
	{
		System.out.println("[ Logged out. ]");
		System.exit(0);
	}
	
	public void setDescription(String string)
	{
		if ("".equals(string)) return;
		System.out.println("[ Description: "+string+" ]");
	}
	
	public void hears(String string)
	{
		System.out.println("< "+string);
	}
	
	public void setName(Vector name)
	{
		System.out.print("[ Name: ");
		Enumeration e = name.elements();
		while(e.hasMoreElements())
		{
			System.out.print(" "+e.nextElement());
		}
		System.out.println(" ]");
	}
	
	public void setExits(Vector exits)
	{
		System.out.print("[ Obvious Exits: ");
		Enumeration e = exits.elements();
		while(e.hasMoreElements())
		{
			System.out.print(" "+e.nextElement());
			if (e.hasMoreElements()) System.out.print(",");
		}
		System.out.println(" ]");
	}

	public void addItem(String item, String container, String desc)
	{
		System.out.println ("[ Item: "+item+" "+desc+" ]");
	}
	
	public void removeItem(String item, String container)
	{
		System.out.println("[ Removed Item: "+item+" ]");
	}
	
	public void enterItem(String item, String container, String desc)
	{
		System.out.println("[ Item Entered: "+item+" "+desc+" ]");
	}
	
	public void leaveItem(String item, String container, String desc)
	{
		System.out.println("[ Item Left: "+item+" "+desc+" ]");
	}
	
	public void clearItems()
	{
		System.out.println("[ Items Cleared. ]");
	}
	
	Faucet mf;
	public void setFaucet(Faucet f)
	{
		mf=f;
	}
	static BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

	public void run()
	{
		try
		{
			String sr = "not null";
			completeAction();
			while(true)
			{
				mf.parseInput(br.readLine());
				
			}
		}
		catch(IOException ioe)
		{
			handleError(ioe);
		}
	}
	public static void main(String[] args) throws IOException
	{
		SystemNozzle sn = new SystemNozzle();
		System.out.print("User: "); System.out.flush();
		String user = br.readLine();
		System.out.print("Password: "); System.out.flush();
		String password = br.readLine();
		System.out.print("Host: "); System.out.flush();
		String host = br.readLine();
		
		Faucet f = new Faucet(sn,user,host,8889,password);
		f.start();
		sn.setFaucet(f);
		new Thread(sn).start();
	}
}
