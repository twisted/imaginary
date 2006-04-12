package twisted.reality.client;

import java.io.*;
import java.net.*;
import java.util.*;
import twisted.util.*;
import com.apple.mrj.*;

public class Faucet extends Thread
{
	public static final int protoVer = 3;
	public static final String version = "1.2.1";
	
	static final int CMD_Hears = 1;
	static final int CMD_SetName = 2;
	static final int CMD_SetPict = 3;
	static final int CMD_SetTheme = 4;
	static final int CMD_RequestResponse = 5;
	static final int CMD_ReturnResponse = 5;
	static final int CMD_CompletedAction = 6;
	static final int CMD_Quit = 7;
	static final int CMD_Exits = 8; // new to V3
	static final int CMD_DisplayErrorDialog = 9; // new to V3
	static final int CMD_Ping = 10; // new to V3
	static final int CMD_Pong = 11; // new to V3
	
	static final int CMD_DescClear = 100;
	static final int CMD_DescAppend = 101;
	static final int CMD_DescRemove = 102;
	
	static final int CMD_ListClear = 110;
	static final int CMD_ListAdd = 111;
	static final int CMD_ListRemove = 112;
	static final int CMD_ListEnter = 113;
	static final int CMD_ListLeave = 114;
	
	static final int CMD_CXStart = 120;
	static final int CMD_CXData = 121;
	static final int CMD_CXStop = 122;
	static final int CMD_CXRequestStop = 122;
	static final int CMD_CXSupported = 123; // new to V3	
	
	static final byte TYPE_None = 0;	
	static final byte TYPE_String = 1;
	static final byte TYPE_RawData = 2;
	
	public static final int TT_STRING = 34;
	public static final int TT_WORD = -3;
	public static final int TT_NUMBER = -2;
	public static final int TT_EOF = -1;
	public static final int TT_EOL = '\n';
	
	public void gotResponse(String responseGot, String key)
	{
		String[] resp = {key, responseGot};
		send(CMD_ReturnResponse, resp);	
	}
	
	public void run()
	{
		/// System.out.println("Running faucet...");
		String rs;
		promptNum=0;
		
		rmdesc=new Hashtable(20);
		
		try
		{
			serverSocket = new Socket(svr,port);
			in = new DataInputStream(serverSocket.getInputStream());
			out = new DataOutputStream(serverSocket.getOutputStream());
			String tst = in.readUTF();
			if(!tst.equals("VERSION"))
			{
				disconnect();
				throw new ConnectException("The server must be too busy or something.");
			}
			out.writeShort(protoVer);
			
			remoteProtoVer = in.readShort();
			if(remoteProtoVer != protoVer)
			{
				disconnect();
				if(remoteProtoVer < protoVer)
					throw new ConnectException("The server is older than this client and thus incompatible. Please use an older Faucet or tell the owners to upgrade their server.");
				else
					throw new ConnectException("The server is incompatible with this version of Faucet. Please upgrade if you wish to connect.");
			}
			tst = in.readUTF();
			if(!tst.equals("LOGIN"))
			{
				disconnect();
				throw new ConnectException("The server returned an unexpected result: " + tst + ".");
			}
			out.writeUTF(usr);
			out.writeUTF(passwd);
			
			tst = in.readUTF();
			if (tst.equals("BADPASS"))
			{
				disconnect();
				throw new ConnectException("Your username or password was incorrect.");
			}
			else if(tst.equals("CONNECTED"))
			{
				isConnected = true;
			}
			else
				throw new ConnectException("The server returned an unexpected result: " + tst + ".");
		}
		catch(IOException ioe)
		{
			nozzle.handleError(ioe);
			nozzle.logout();
			stop();
		}
		catch(ConnectException ioe)
		{
			nozzle.handleError(ioe);
			nozzle.logout();
			stop();
		}
		
		try
		{
			final Vector arg = new Vector();
			final Faucet realThis = this;
		readloop:
			for(;;)
			{
				final int command=recieve(arg);
				switch (command)
				{
					
				case CMD_Ping:
					send(CMD_Pong, arg);
					break;
					
				case CMD_Hears:
					nozzle.hears((String)arg.elementAt(0));
					break;
					
				case CMD_SetName:
					nozzle.setName(arg);
					break;
				case CMD_SetPict:
					// nozzle.setPicture(arg);
					break;
					
				case CMD_Exits:
					nozzle.setExits(arg);
					break;
					
				case CMD_DescAppend:
					adddescript((String)arg.elementAt(0), (String)arg.elementAt(1));
					break;
					
				case CMD_DescRemove:
					removedescript((String)arg.elementAt(0));
					break;
					
				case CMD_DescClear:
					cleardescript();
					break;
					
				case CMD_ListClear:
					nozzle.clearItems();
					break;
					
				case CMD_ListAdd:
					/* element at 0: identifier
					   element at 1: parent identifier
					   element at 2: description
					*/
					// additem((String)arg.elementAt(0), (String)arg.elementAt(1), (String)arg.elementAt(2));
					nozzle.addItem((String) arg.elementAt(0), (String) arg.elementAt(1), (String) arg.elementAt(2));
					break;
				case CMD_ListLeave:
					/* element at 0: identifier
					   element at 1: parent identifier
					   element at 2: descriptive text
					*/
					// leaveitem((String)arg.elementAt(0), (String)arg.elementAt(1), (String)arg.elementAt(2));
					nozzle.leaveItem((String) arg.elementAt(0), (String) arg.elementAt(1), (String) arg.elementAt(2));
					break;
				case CMD_ListEnter:
					/* element at 0: identifier
					   element at 1: parent identifier
					   element at 2: descriptive text
					*/
					// enteritem((String)arg.elementAt(0), (String)arg.elementAt(1), (String)arg.elementAt(2));
					nozzle.enterItem((String) arg.elementAt(0), (String) arg.elementAt(1), (String) arg.elementAt(2));
					break;
				case CMD_ListRemove:
					// removeitem((String)arg.elementAt(0), (String)arg.elementAt(1));
					/* element at 0: identifier
					   element at 1: parent identifier
					*/
					nozzle.removeItem((String)arg.elementAt(0), (String) arg.elementAt(1));
					break;
				case CMD_CompletedAction:
					nozzle.completeAction();
					break;
				case CMD_CXData:
				{
					Integer cxnum = Integer.valueOf((String)arg.elementAt(0));
					arg.removeElementAt(0);
					Object[] m = new Object[arg.size()];
					arg.copyInto(m);
					CX cx = (CX)cXes.get(cxnum);
					if(cx == null) System.out.println("BUG! CX " + cxnum + " hasn't been loaded!");
					cx.handleData(m);
				}
				break;
				
				case CMD_DisplayErrorDialog:
					nozzle.dialog((String)arg.elementAt(0));
					break;
					
				case CMD_CXSupported:
					// bad implementation...fix later. should return a property or something.
					send(CMD_CXSupported, "all");
					break;
					
				case CMD_RequestResponse:
				{
					String num =   (String)arg.elementAt(0);
					String prmpt = (String)arg.elementAt(1);
					String defvl = (String)arg.elementAt(2);
					
					nozzle.requestResponse(num,prmpt,defvl);
				}
				break;
				case CMD_SetTheme:
					nozzle.setTheme((String)arg.elementAt(0));
					break;
				case CMD_CXStart:
					try
					{
						String theClass = (String)arg.elementAt(0);
						Integer cxnum = Integer.valueOf((String)arg.elementAt(1));
						Class ccx = Class.forName(theClass);
						CX cx = (CX)ccx.newInstance();
						cx.setStub(gStub, cxnum.intValue());
						cXes.put(cxnum, cx);
						cx.init();
						
					}
					catch (Exception e)
					{
						System.out.println("Error loading client extension:" + arg);
						System.out.println(e);
					}
					break;
				case CMD_CXStop:
					Integer cxnum = Integer.valueOf((String)arg.elementAt(0));
					CX cx = (CX)cXes.get(cxnum);
					if(cx == null) System.out.println("BUG! CX " + cxnum + " hasn't been loaded!");
					cx.destroy();
					cXes.remove(cxnum);
					break;
				case CMD_Quit:
					isConnected = false;
					nozzle.logout();
					break readloop;
				}
			}
		}
		catch(SocketException se)
		{
			// Do nothing here, it's A-O.K. :)
		}
		catch(EOFException e)
		{
		}
		catch(IOException e)
		{
			nozzle.dialog("Network Difficulty: " + e);
			e.printStackTrace();
		}
		finally
		{
			disconnect();
		}
	}

	private String __main__;
	
	private void adddescript(String name, String desc)
	{
		if (name.intern()=="__MAIN__")
		{
			__main__=desc;
		}
		else
		{
			rmdesc.put(name, desc);
		}
		refreshDesc();
	}
	
	private void cleardescript()
	{
		rmdesc=new Hashtable(20);
		__main__ = "";
		refreshDesc();
	}
	
	private void removedescript(String rs)
	{
		rmdesc.remove(rs);
		refreshDesc();
	}
	
	private void refreshDesc()
	{
		synchronized(rmdesc)
		{
			StringBuffer temp = new StringBuffer();
			temp.append(__main__);
			Enumeration e = rmdesc.elements();
			while(e.hasMoreElements())
			{
				temp.append(' ');
				temp.append(e.nextElement());
			}
			nozzle.setDescription(temp.toString());
		}
	}
	
	public void bye()
	{
		if (isConnected)
		{
			send (CMD_Quit);
			disconnect();
		}
	}
	
	public void parseInput(String str)
	{
		/*
		  if(str.charAt(0)=='@')
		  {
		  if(str.startsWith("@q"))
		  {
		  }
		  if(str.startsWith("@d"))
		  {
		  send(CMD_Quit);
		  disconnect();
		  }
		  return;
		  }
		*/
		int space = str.indexOf(" ");
		String command = (space == -1)?str:str.substring(0, space);
		if(shortcuts.containsKey(command))
		{
			String arg = (space == -1)?"":str.substring(space + 1);
			command=(String)shortcuts.get(command);
			str = command + " " + arg;
		}
		parseAction(str);
	}

	Nozzle nozzle;

	String usr;
	String svr;
	int port;
	String passwd;

	public Faucet(Nozzle inNozzle, String iusr, String isvr, int iport, String ipasswd)
	{		
		nozzle=inNozzle;
		usr=iusr;
		port=iport;
		svr=isvr;
		passwd=ipasswd;

		gStub = new CXStub(this);
		cXes = new Hashtable();
		
		shortcuts = new Hashtable(20);
	
		shortcuts.put("n","go north");
		shortcuts.put("north","go north");
		shortcuts.put("ne","go northeast");
		shortcuts.put("northeast","go northeast");
		shortcuts.put("e","go east");
		shortcuts.put("east","go east");
		shortcuts.put("se","go southeast");
		shortcuts.put("southeast","go southeast");
		shortcuts.put("s","go south");
		shortcuts.put("south","go south");
		shortcuts.put("sw","go southwest");
		shortcuts.put("southwest","go southwest");
		shortcuts.put("w","go west");
		shortcuts.put("west","go west");
		shortcuts.put("nw","go northwest");
		shortcuts.put("northwest","go northwest");
		shortcuts.put("u","go up");
		shortcuts.put("up","go up");
		shortcuts.put("d","go down");
		shortcuts.put("down","go down");
		
		shortcuts.put("l","look");
		shortcuts.put("i","inventory");
	
		isConnected = false;
	}
	
	
	public void parseAction(String str)
	{
		nozzle.hears("> " + str);
		if (str==null) return;
		if (str.equals("")) return;
		promptNum++;
		// reprompt();
		
		send(CMD_Hears, str);
	}
	
	public static void main(String[] args)
	{
		SwingNozzle.main(args);
	}
	

	public void disconnect()
	{
		if(isConnected)
		{
			isConnected=false;
			try
			{
				serverSocket.close();
			}
			catch(Exception e)
			{
				
			}
			serverSocket = null;
			nozzle.logout();
		}
	}
	
	protected byte[] readBytes() throws IOException
	{
		int length = in.readShort();
		
		byte[] b = new byte[length];
		int readlen = in.read(b, 0, length);
		// throw exception if end of stream reached before it was expected.
		/* kaffe breaks here */
		if (readlen < length) throw new IOException();
		return b;
	}
	
	protected void writeBytes(byte[] b, int len) throws IOException
	{
		out.writeShort(len);
		out.write(b, 0, len);
	}
	
	public int recieve(Vector result) throws IOException
	{
		result.removeAllElements();
		
		int command = in.readShort();
		int parts = in.readUnsignedByte();
		
		for (int i = 0; i < parts; i++)
		{
			byte type = in.readByte();
			switch (type)
			{
				case TYPE_None:
					result.addElement(null);
					break;
				case TYPE_String:
					result.addElement(in.readUTF());
					break;
				case TYPE_RawData:
					result.addElement(readBytes());
				default:
					throw new IOException("Unknown data type!");
			}
		}
		return command;
	}
	
	public synchronized void send(int command, Vector data)
	{
		try
		{
			int length = data.size();
			out.writeShort(command);
			out.writeByte(length);
			
			for (int i = 0; i < length; i++)
			{
				Object o = data.elementAt(i);
				if(o instanceof String)
				{
					out.writeByte(TYPE_String);
					out.writeUTF((String)o);
				} else if(o instanceof byte[])
				{
					out.writeByte(TYPE_RawData);
					writeBytes((byte[])o, ((byte[])o).length);
				}
				else
				{
					System.out.println("Programmers are stupid, eh? (Tried to send an unknown type of data)");
					out.writeByte(TYPE_None);
				}
			}
			out.flush();
		}
		catch(IOException ieee)
		{
			disconnect();
		}
	}
	
	public synchronized void send(int command, Object[] data)
	{
		try
		{
			int length = data.length;
			out.writeShort(command);
			out.writeByte(length);
			
			for (int i = 0; i < length; i++)
			{
				Object o = data[i];
				if(o instanceof String)
				{
					out.writeByte(TYPE_String);
					out.writeUTF((String)o);
				} else if(o instanceof byte[])
				{
					out.writeByte(TYPE_RawData);
					writeBytes((byte[])o, ((byte[])o).length);
				}
				else
				{
					System.out.println("Programmers are stupid, eh? (Tried to send an unknown type of data)");
					out.writeByte(TYPE_None);
				}
			}
			out.flush();
		}
		catch(IOException ieee)
		{
			disconnect();
		}
	}

	public synchronized void send(int command, String data)
	{
		try
		{
			out.writeShort(command);
			/* 
			 * For the easily confused (from glyph)
			 * 
			 * When I saw this line I was a tad confused, but think of
			 * it as a special-case for a vector / array of length 1.
			 */
			out.writeByte(1);
			
			out.writeByte(TYPE_String);
			out.writeUTF(data);
			out.flush();
		}
		catch(IOException ieee)
		{
			disconnect();
		}
	}
	
	public synchronized void send(int command)
	{
		try
		{
			out.writeShort(command);
			out.writeByte(0);
			out.flush();
		}
		catch(IOException ieee)
		{
			disconnect();
		}
	}
	
	private CXStub gStub;
	private Hashtable cXes;
	
	private int promptNum;
	private Hashtable rmdesc;
	
	private Hashtable shortcuts;

	private boolean isConnected;
	private Socket serverSocket;
	private DataOutputStream	out;
	private DataInputStream		in;
	private int remoteProtoVer;
}
