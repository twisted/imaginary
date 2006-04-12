package twisted.reality;

import java.io.*;
import java.net.*;
import java.util.*;
import twisted.util.StringLegalizer;
import twisted.util.UnixCrypt;

/**
 * An implementation of VERSION 2 of the Reality Server protocol
 * 
 * @author James Knight
 */

class NetClientUserV2 extends RealityUI
{
	public static final int protoVer = 2;
	
	static final int CMD_Hears = 1;
	static final int CMD_SetName = 2;
	static final int CMD_SetPict = 3;
	static final int CMD_SetTheme = 4;
	static final int CMD_RequestResponse = 5;
	static final int CMD_ReturnResponse = 5;
	static final int CMD_CompletedAction = 6;
	static final int CMD_Quit = 7;
	
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
	
	static final byte TYPE_None = 0;	
	static final byte TYPE_String = 1;
	static final byte TYPE_RawData = 2;
	
	public NetClientUserV2(Socket i, int c, int remoteVer)
	{
		remoteProtoVer = remoteVer;
		incoming = i; counter = c;
		quitsent=false;
		try
		{
			incoming.setSoTimeout(120000); // 2 minutes
			in	= new DataInputStream(incoming.getInputStream());
			out = new DataOutputStream(incoming.getOutputStream());
		}
		catch (Exception e)
		{
			Age.log("Couldn't get inputStream on ClientUser! Aargh!");
			e.printStackTrace();
		}
		startThread();
	}
	
	public NetClientUserV2(Socket i, int c)
	{
		this(i,c,0);
	}
	
	public synchronized void requestResponse(Long l,String s,String r)
	{
		String[] data = {String.valueOf(l),s,r};
		send(CMD_RequestResponse, data);
	}
	
	public synchronized void theme(String s)
	{
		send(CMD_SetTheme, ((s!=null)?s:"default"));
	}
	
	public synchronized void hears(String s)
	{
		send(CMD_Hears, s);
	}
	/*	
		public void sees(String s)
		{
		if(s != null) send(CMD_SetPict, s);
		else send(CMD_SetPict, "none");
		}
	*/
	
	String exitsToDescriptionKludge(Room r)
	{
		StringBuffer s = new StringBuffer("\nObvious Exits: ");
		
		Enumeration e = r.allPortals();
		
		boolean isFirst = true;
		if(e!=null)
		{
			while(e.hasMoreElements())
			{
				Portal p = (Portal) e.nextElement();
				// TODO: put in some way to tell if the exit is visible...
				if( !p.isObvious() )
				{
					continue;
				}
				if(isFirst)
				{
					isFirst=false;
				}
				else
				{
					s.append(", ");
				}
				s.append(p.name());
			}
		}
		
		return s.toString();
	}

	public synchronized void setFocus(Thing th)
	{
		if(th!=null)
		{
			theme(th.getTheme());
			if(th!=who().place())
				send(CMD_SetName, who().place().nameTo(who())+": "+th.nameTo(who()));
			else
				send(CMD_SetName, th.nameTo(who()) );
			
			
			/*if(th.getImage() != null) send(CMD_SetPict, th.getImage());
			else { send(CMD_SetPict, "none"); }*/
			
			clearList();
			
			clearDescript();
			
			notifyDescriptAppend("__MAIN__", th.describeTo(who()));
			
			Enumeration theE = th.descriptionElements();
			if(theE!=null)
			{
				Enumeration Etwo = th.descriptionKeys();
				while(theE.hasMoreElements())
				{
					String theO = who().fromMyPerspective(theE.nextElement());
					String theK = (String) Etwo.nextElement();
					
					notifyDescriptAppend(theK,theO);
				}
			}
			
			if (th instanceof Room)
			{
				if( !th.getBool("inhibit_exits") )
					notifyDescriptAppend("__EXITS_KLUDGE__", exitsToDescriptionKludge((Room)th));
			}
			if (th instanceof Location) 
			{
				Location rm = (Location) th;
				listStuff(rm);
			}
		}
	}
	
	public synchronized void listStuff(Location rom)
	{
		if( (rom.inventory != null) && rom.areContentsVisible())
		{
			Enumeration e = rom.inventory.elements();
			
			while(e.hasMoreElements())
			{
				Thing inQuestion = (Thing) e.nextElement();
				if(inQuestion != who() && !inQuestion.isComponent())
					notifyEntered(inQuestion, rom);
			}
		}
	}
	
	public synchronized void clearList()
	{
		numThingMap.setSize(0);
		send(CMD_ListClear);
	}
	
	public synchronized void clearDescript()
	{
		send(CMD_DescClear);
	}
	public synchronized void notifyDescriptAppend(String theKey, String theData)
	{
		String[] data = {theKey, theData};
		send(CMD_DescAppend, data);
	}
	public synchronized void notifyDescriptRemove(String theKey)
	{
		send(CMD_DescRemove, theKey);
	}
	
	Vector numThingMap = new Vector();
	String thingToIdent(Thing th)
	{
		if(th == null) return "none";
		int num = numThingMap.indexOf(th);
		if(num == -1)
		{
			numThingMap.addElement(th);
			num = numThingMap.size() - 1;
		}
		return String.valueOf(num);
	}
	
	Thing identToThing(String ident)
	{
		if (ident.equals("none")) return null;
		int num = Integer.parseInt(ident);
		if (num >= 0 && num < numThingMap.size())
			return (Thing)numThingMap.elementAt(num);
		return null;
	}
	
	synchronized void notifyEntered(Thing th, Thing inth)
	{
		String[] data = {thingToIdent(th), th.isHereTo(who())};
		send(CMD_ListAdd, data);
	}
	
	synchronized void notifyLeaving(Thing th, Thing inth, String str)
	{
		String[] data = {thingToIdent(th), str};
		send(CMD_ListLeave, data);
	}
	
	synchronized void notifyEntering(Thing th, Thing inth, String str)
	{
		String[] data = {thingToIdent(th), str};
		send(CMD_ListEnter, data);
	}
	
	synchronized void notifyLeft(Thing th, Thing inth)
	{
		send(CMD_ListRemove, thingToIdent(th));
	}
	
	public void run()
	{
		Player plr=null;
		try
		{
			//boolean isnew=false;

			if(remoteProtoVer == 0) // if we don't already have the version
			{
				out.writeUTF("VERSION");
				remoteProtoVer = in.readShort();
			}
			/* here is where you would transfer control to another RealityUI if you wanted
			 * to support an old version of the client. e.g.
			 * if(remoteProtoVer != protoVer)
			 *	 new OtherUserThingie(socket, etc..); return;
			 * If the Faucet sees a protocol version that doesn't match its it will refuse
			 * to connect.
			 */
			out.writeShort(protoVer);
			out.writeUTF("LOGIN");
			String player = in.readUTF();
			String pass = in.readUTF();
			
			Thing thin = Age.theUniverse().findThing(player);
			if( ( thin != null) && (thin instanceof Player))
			{
				plr=(Player) thin;
				
				if(!plr.password.equals(UnixCrypt.crypt(pass,plr.password)))
				{
					out.writeUTF("BADPASS");
					
					incoming.close();
					Age.log("Bad password for user " + player + "!");
					return;
				}
			}
			else
			{
				out.writeUTF("BADPASS");
				
				incoming.close();
				Age.log("Bad username: " + player + "!");
				return;
			}
			
			Age.log(plr.name() + "@" + incoming.getInetAddress().getHostName() + " has connected (using the V2 protocol).");
			out.writeUTF("CONNECTED");
			Age.theUniverse().connect(plr, this);
			
			Vector arg = new Vector();
		readloop:
			for(;;)
			{
				Thread.sleep(250);
				//		  Age.log("The line that was read was: \n"+StringLegalizer.legalize(st)+"\nFrom: "+plr.name());
				int command;
				try
				{
					command = recieve(arg);
				} catch (InterruptedIOException e) {
					if(!Thread.interrupted())
						continue readloop;
					else
						break readloop;
				}
				if(quitsent) break readloop;
				switch(command)
				{
					case CMD_Hears:
						delayAndExecute((String)arg.elementAt(0));
						send(CMD_CompletedAction);
						break;
					case CMD_ReturnResponse:
						try
						{
							Long l = Long.valueOf((String)arg.elementAt(0));
							String st=(String)arg.elementAt(1);
							who().gotResponse(st,l);
						}
						catch(RuntimeException e)
						{
							hears("Serverside error!!! You've found a bug.\n" + e);
							Age.log("Server-side bug detected:");
							e.printStackTrace();
						}
						break;
					case CMD_Quit:
						// Age.log("Recieved CMD_Quit from client.");
						quitsent=true;
						break readloop;
				}
			}
		}
		catch(SocketException seocket)
		{
			if (plr != null)
			{
				Age.log(plr.name() + " *appears* to have logged out correctly.");
			}
			else
			{
				Age.log("Socket death in login on "+counter+".");
			}
		}
		catch(IOException e)
		{
			Age.log(e);
			if(plr!=null)
			{
				Age.log(plr.name()+" got booted");
			}
			else
				Age.log("IOException in login on " + counter + ".");
		}
		catch(InterruptedException what)
		{
			Age.log(plr.name() + " Interrupted... HALTING THREAD.");
			return;
		}
		catch(Exception ieee)
		{
			Age.log("Ieee!!! "+ieee);
			ieee.printStackTrace();
			if(plr!=null)
				Age.log(plr.name()+" died an exception death.");
			else
				Age.log("Unknown error - dead player thread disconnected.");
		}
		if(who() != null)
			Age.theUniverse().disconnect(who());
	}
	boolean quitsent;
	synchronized void dispose()
	{
		String name = (who() == null)?"Unknown user":who().name();
		myPlayer = null;
		if (!quitsent) { quitsent=true; send(CMD_Quit); }
		Age.log("Stopping " + counter + " on Reality.");
		try{incoming.close();}catch(Exception e){/*who cares?*/}
		Age.log(name + ":"+counter+" disconnected");
		
		t.interrupt();
	}
	
	private void disconnect(Exception e)
	{
		Age.log("Yipe!!! IO error.");
		Age.log(e.toString());
		e.printStackTrace();
		if(who() != null)
			Age.theUniverse().disconnect(who());
		/* that's all, folks */
	}
	
	synchronized byte[] readBytes() throws IOException
	{
		int length = in.readShort();
		
		byte[] b = new byte[length];
		int readlen = in.read(b, 0, length);
		// throw exception if end of stream reached before it was expected.
		if (readlen < length) throw new IOException();
		return b;
	}
	
	synchronized void writeBytes(byte[] b, int len) throws IOException
	{
		out.writeShort(len);
		out.write(b, 0, len);
	}

	int recieve(Vector result) throws IOException
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
	
	synchronized void send(int command, Vector data)
	{
		try
		{
			int length = data.size();
			out.writeShort(command);
			out.writeByte(length);
			
			for (int i = 0; i < length; i++)
			{
				Object o = data.elementAt(i);
				if(o == null)
				{
					out.writeByte(TYPE_None);
					System.out.println("You probably didn't really want to write that null value, right?");
					Thread.dumpStack();
				}
				else if(o instanceof String)
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
		catch(Exception ieee)
		{
			disconnect(ieee);
		}
	}
	
	synchronized void send(int command, String data)
	{
		if(data==null)
		{
			data="null";
			System.out.println("You probably didn't really want to write that null value, right?");
			Thread.dumpStack();
		}
		try
		{
			out.writeShort(command);
			out.writeByte(1);
			
			out.writeByte(TYPE_String);
			out.writeUTF(data);
			out.flush();
		}
		catch(Exception ieee)
		{
			disconnect(ieee);
		}
	}
	
	synchronized void send(int command, Object[] data)
	{
		try
		{
			int length = data.length;
			out.writeShort(command);
			out.writeByte(length);
			
			for (int i = 0; i < length; i++)
			{
				Object o = data[i];
				if(o == null)
				{
					out.writeByte(TYPE_None);
					System.out.println("You probably didn't really want to write that null value, right?");
					Thread.dumpStack();
				}
				else if(o instanceof String)
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
			disconnect(ieee);
		}
	}
	
	synchronized void send(int command)
	{
		try
		{
			out.writeShort(command);
			out.writeByte(0);
			out.flush();
		}
		catch(Exception ieee)
		{
			disconnect(ieee);
		}
	}

	byte[] inbuffer = new byte[512];
	int remoteProtoVer;
	Socket incoming;
	int counter;
	DataInputStream in;
	DataOutputStream out;
	Hashtable CXHandlers;
	int cxnum = 0;
}
