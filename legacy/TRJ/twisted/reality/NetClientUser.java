package twisted.reality;

import java.io.*;
import java.net.*;
import java.util.*;
import twisted.util.StringLegalizer;
import twisted.util.UnixCrypt;
import twisted.util.QueueEnumeration;
/**
 * An implementation of VERSION 3 of the Reality Server protocol
 * 
 * @author James Knight
 */

class NetClientUser extends RealityUI
{
	public static final int protoVer = 3;
	
	static final int CMD_Hears = 1;
	static final int CMD_SetName = 2; // uses Vector in V3
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
	
	NetClientUser(Socket i, int c, int remoteVer)
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
	
	NetClientUser(Socket i, int c)
	{
		this(i,c,0);
	}

	synchronized void requestResponse(Long l,String s,String r)
	{
		String[] data = {String.valueOf(l),s,r};
		send(CMD_RequestResponse, data);
	}
	
	synchronized void theme(String s)
	{
		send(CMD_SetTheme, ((s!=null)?s:"default"));
	}
	
	synchronized void hears(String s)
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

	final Vector tempVector = new Vector();
	synchronized void setFocus(Thing th)
	{
		Player w = who();
		if(th!=null)
		{
			theme(th.getTheme());
			
			tempVector.setSize(0);
			if ( w.place().isBroadcast() )
			{
				for(Thing t=th;
					t != null && t != w.place() && t != w.topPlace();
					t=t.place())
					
					tempVector.addElement(t.nameTo(w));
				
				tempVector.addElement(w.topPlace().nameTo(w)+" ("+w.getPrepTo(w)+" "+w.place().the()+w.place().nameTo(w)+")");
				
			}

			else for(Thing t=th;
					t != null && t != w.place().place();
					t = t.place())
				
					tempVector.addElement(t.nameTo(w));
			
			send(CMD_SetName, tempVector);
			
			/*if(th.getImage() != null) send(CMD_SetPict, th.getImage());
			else { send(CMD_SetPict, "none"); }*/
			
			clearList();
			
			clearDescript();
			
			notifyDescriptAppend("__MAIN__", th.describeTo(w));
			
			Enumeration theE = th.descriptionElements();
			if(theE!=null)
			{
				Enumeration Etwo = th.descriptionKeys();
				while(theE.hasMoreElements())
				{
					String theO = w.fromMyPerspective(theE.nextElement());
					String theK = (String)Etwo.nextElement();
					
					notifyDescriptAppend(theK,theO);
				}
			}
			
			if (th instanceof Room)
			{
				tempVector.setSize(0);
				for (Enumeration e = ((Room)th).allPortals(); e.hasMoreElements(); )
				{
					Portal p = (Portal) e.nextElement();
					if (p.isObvious())
						tempVector.addElement(p.name());
				}
				send(CMD_Exits, tempVector);
			}

			if (th instanceof Location) 
			{
				Location rm = (Location) th;
				listStuff(rm);
			}
		}
		/* For some reason, my focus is getting set AFTER I've been
		  disconnected, which makes this crash!  You take the wooden
		  wood.

		  else { send(CMD_SetName,"Nowhere"); send(CMD_Exits,new
		  Vector()); clearList(); clearDescript();
		  notifyDescriptAppend("__MAIN__","You are currently in a null
		  location.  You will likely be logged out."); } */
	}
	
	synchronized void clearDescript()
	{
		send(CMD_DescClear);
	}
	synchronized void notifyDescriptAppend(String theKey, String theData)
	{
		String[] data = {theKey, theData};
		send(CMD_DescAppend, data);
	}
	synchronized void notifyDescriptRemove(String theKey)
	{
		send(CMD_DescRemove, theKey);
	}
	
	/*
	  This is a temporary hack -- in the future, every object should
	  be sent, and the client should put them into the proper order.
	  However, while we're waiting to find out what the final client
	  looks like, we're going to use this so that people seated in
	  furniture or vehicles show up if they're supposed to.
	 */
	
	class ListStuffEnum extends QueueEnumeration
	{
		ListStuffEnum(Enumeration e)
		{
			while (e.hasMoreElements())
			{
				Object o = e.nextElement();
				enQueue(o);
				if (o instanceof Location)
				{
					Location l = (Location) o;
					if (l.isBroadcast() && l.inventory != null)
					{
						Enumeration alt = l.inventory.elements();
						if (alt != null)
						{
							Enumeration alte = new ListStuffEnum(alt);
							while (alte.hasMoreElements())
							{
								enQueue(alte.nextElement());
							}
						}
					}
				}
			}
		}
	}
	
	synchronized void listStuff(Location rom)
	{
		if((rom.inventory != null) && (rom.areContentsVisible()))
		{
			Enumeration e = rom.inventory.elements();
			// temporary hack described above.
			e=new ListStuffEnum(e);
			while(e.hasMoreElements())
			{
				Thing inQuestion = (Thing) e.nextElement();
				if(inQuestion != who() && !inQuestion.isComponent())
					notifyEntered(inQuestion, inQuestion.place());
			}
		}
	}
	
	synchronized void clearList()
	{
		numThingMap.setSize(0);
		send(CMD_ListClear);
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
		// this is here so that the container id comes first, so that the focus
		// is always id 0. (same in all other notify's)
		String inthid = thingToIdent(inth);
		Object[] data = {thingToIdent(th), inthid, th.isHereTo(who())};
		send(CMD_ListAdd, data);
	}
	
	synchronized void notifyLeaving(Thing th, Thing inth, String str)
	{
		String inthid = thingToIdent(inth);
		String[] data = {thingToIdent(th), inthid, str};
		send(CMD_ListLeave, data);
	}
	
	synchronized void notifyEntering(Thing th, Thing inth, String str)
	{
		String inthid = thingToIdent(inth);
		String[] data = {thingToIdent(th), inthid, str};
		send(CMD_ListEnter, data);
	}
	
	synchronized void notifyLeft(Thing th, Thing inth)
	{
		String inthid = thingToIdent(inth);
		String[] data = {thingToIdent(th), inthid};
		send(CMD_ListRemove, data);
	}
	
	synchronized boolean clientSupportsCX(String cx)
	{
		/*FIXME*/
		return true;
	}
	
	synchronized void startCX(CXHandler c)
	{
		String clclass = c.getClientClass();
		if(!clientSupportsCX(clclass)) throw new RealClientException("The client doesn't support CX " + clclass + ".");
		Integer i = new Integer(cxnum++);
		c.init(this, i);
		CXHandlers.put(i, c);
		String[] data = {clclass, String.valueOf(i)};
		send(CMD_CXStart, data);
	}
	
	synchronized void sendCXData(Object cxnum, String message)
	{
		String[] m = {cxnum.toString(), message};
		send(CMD_CXData, m);
	}

	synchronized void sendCXData(Object cxnum, Object[] message)
	{
		Object[] m = new Object[message.length+1];
		System.arraycopy(message, 0, m, 1, message.length);
		m[0] = cxnum.toString();
		send(CMD_CXData, m);
	}
	
	synchronized void stopCX(Object cxnum)
	{
		CXHandler cx = (CXHandler)CXHandlers.get(cxnum);
		if(cx == null) System.out.println("BUG! CX " + cxnum + " hasn't been loaded!");
		send(CMD_CXStop, cxnum.toString());
		cx.destroy();
		CXHandlers.remove(cxnum);
	}
	
	synchronized void errorMessage(String message)
	{
		send(CMD_DisplayErrorDialog, message);
	}
	
	public void run()
	{
		Player plr=null;
		boolean sentping = false;
		CXHandlers = new Hashtable();
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
			if(remoteProtoVer == 2)
			{
				new NetClientUserV2(incoming, counter, remoteProtoVer);
				return;
			}
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
			
			Age.log(plr.name() + "@" + incoming.getInetAddress().getHostName() + " has connected.");
			out.writeUTF("CONNECTED");
			// Age.log(plr.name() + " is not broken");
			Age.theUniverse().connect(plr, this);
			
			Vector arg = new Vector();
		readloop:
			for(;;)
			{
				Thread.sleep(250);
				int command;
				try
				{
					command = recieve(arg);
				} catch (InterruptedIOException e) {
					if(!sentping && !Thread.interrupted())
					{
						sentping = true;
						send(CMD_Ping, "");
						continue readloop;
					}
					else
						break readloop;
				}
				//if for some reason interrupt didn't work, stop the thread now.
				if(quitsent) break readloop;
				sentping = false;
				switch(command)
				{
					case CMD_Hears:
						delayAndExecute((String)arg.elementAt(0));
						if(Thread.interrupted()) break readloop;
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
					case CMD_CXData:
					{
						Integer connection = Integer.valueOf((String)arg.elementAt(0));
						arg.removeElementAt(0);
						Object[] m = new Object[arg.size()];
						arg.copyInto(m);
						CXHandler cx = (CXHandler)CXHandlers.get(connection);
						if(cx == null) Age.log("Frink! CX " + connection + " hasn't been loaded!");
						cx.handleData(m);
						break;
					}
					case CMD_CXRequestStop:
					{
						Integer connection = Integer.valueOf((String)arg.elementAt(0));
						CXHandler cx = (CXHandler)CXHandlers.get(connection);
						if(cx == null) Age.log("Frink! CX " + connection + " hasn't been loaded!");
						cx.handleClose();
						break;
					}
					case CMD_Pong:
						break; // do nothing special...just reset sentping.
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
				Age.log(plr.name()+":"+counter+" got booted");
			}
			else
				Age.log("IOException in login on " + counter + ".");
		}
		catch(InterruptedException what)
		{
			Age.log(plr.name() + ":"+counter+" Interrupted... HALTING THREAD.");
		}
		catch(Exception ieee)
		{
			Age.log("Ieee!!! "+ieee);
			ieee.printStackTrace();
			if(plr!=null)
				Age.log(plr.name()+":"+counter+" died an exception death.");
			else
				Age.log("Unknown error - dead player thread disconnected.");
		}
		
		
		// shut down all cxhandlers left over.
		for(Enumeration ecx = CXHandlers.elements(); ecx.hasMoreElements(); )
		{
			CXHandler cx = ((CXHandler)ecx.nextElement());
			
			try
			{
				cx.destroy();
			}
			catch (Exception e)
			{
				Age.log("Error destroying CXHandler " + cx.getClass() + ": " + e);
			}
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
		Age.log("Yipe!!! IO error on "+counter);
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
	int remoteProtoVer = 0;
	Socket incoming;
	int counter;
	DataInputStream in;
	DataOutputStream out;
	Hashtable CXHandlers;
	int cxnum = 0;
}
