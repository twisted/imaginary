package gloop;

import java.util.Hashtable;
import java.util.Vector;
import java.util.Dictionary;

import java.io.IOException;

import java.net.Socket;

public class Gloop extends Glip
{
	public static final int SET=50;
	public static final int GET=51;
	public static final int CALL=52;
	public static final int ANSWER=53;
	public static final int ERROR=54;
	public static final int NAME=55;
	public static final int SUCCESS=0;
	
	private Hashtable answers=new Hashtable();
	private Hashtable errors=new Hashtable();
	private Hashtable registry=new Hashtable();
	private Naming naming;
	
	private int session=0;
	
	public Gloop() {
		this(Naming.default_naming);
	}

	public Gloop(Naming naming) {
		this.naming=naming;
	}

	public Integer requestID() {
		return new Integer(session++);
	}
	
	public Bolg bound(String name) {
		return naming.bound(name);
	}
	
	public void bind(String name, Object obj) {
		naming.bind(name,obj);
	}
	
	public Bolg registered(Integer key) {
		return (Bolg) registry.get(key);
	}

	public Integer register(Object nbolg) {
		if (nbolg instanceof Bolg) 
			return new Integer(((Bolg)nbolg).hashCode());
		Integer i = new Integer(nbolg.hashCode());
		registry.put(i,nbolg);
		return i;
	}

	public Object waitFor(Integer request) throws IOException {
		Object answer = answers.remove(request);
		while(answer==null)
		{
			snarf((Vector)read());
			answer=answers.remove(request);
		}
		if (answer.equals("__NULL__")) return null;
		return answer;
	}
	
	public Object sendGet(Integer object,
						  String key) throws IOException {
		Integer request = requestID();
		Vector v = new Vector();
		v.addElement(new Integer(GET));
		v.addElement(request);
		v.addElement(object);
		v.addElement(key);
		write(v);
		return waitFor(request);
	}
	
	public Object sendCall(Integer object,
						   Object[] args) throws IOException {
		Integer request = requestID();
		Vector v = new Vector();
		v.addElement(new Integer(CALL));
		v.addElement(request);
		v.addElement(object);
		for (int i = 0; i < args.length; i++) {
			v.addElement(args[i]);
		}
		write (v);
		return waitFor(request);
	}

	public Object sendName(String name) throws IOException {
		Integer request = requestID();
		Vector v = new Vector();
		v.addElement(new Integer(NAME));
		v.addElement(request);
		v.addElement(name);
		write (v);
		return waitFor(request);
	}

	public void writeReference(Object toRefer) throws IOException {
		register(toRefer);
		writeInt(toRefer.hashCode());
	}
	
	public Object readReference() throws IOException {
		return new Glob(this,new Integer(readInt()));
	}
	
	public void sendAnswer(Integer request,
						   Object o) throws GloopException {
		try {
			Vector v = new Vector();
			v.addElement(new Integer(ANSWER));
			v.addElement(request);
			v.addElement(o);
			write(v);
		}
		catch(IOException ioe) {
			throw new GloopException("Connection Lost",ioe);
		}
	}

	public void sendError(Integer request,
						  GloopException ge) throws IOException {
		Vector v = new Vector();
		v.addElement(new Integer(ERROR));
		v.addElement(request);
		v.addElement(ge.getMessage());
		v.addElement(ge.getStackTrace());
		write(v);
	}
	
	public void sendSet(Integer object,
						String key,
						Object value) throws IOException {
		Integer request=requestID();
		Vector v = new Vector();
		v.addElement(new Integer(SET));
		v.addElement(request);
		v.addElement(object);
		v.addElement(key);
		v.addElement(value);
		write(v);
		waitFor(request);
	}
	
	public void gotSet(Integer request,
					   Integer object,
					   String member,
					   Object value) throws GloopException {
		try {
			try {
				Bolg bolg = registered(object);
				bolg.set(member,value);
				sendAnswer(request,new Integer(SUCCESS));
			} catch(Exception nsfe) {
				sendError(request, new GloopException("No such field.",nsfe));
			}
		} catch (IOException ioe) {
			throw new ConnectionLost(ioe);
		}
	}
	
	public void gotCall(Integer request,
						Integer object,
						Object[] args) throws ConnectionLost
		throws GloopException{
		try {
			Bolg bolg = registered(object);

			sendAnswer(request,bolg.call(args));
		}
	}
	
	public void gotForget(Integer object) {
		
	}
	
	public void gotGet(Integer request,
					   Integer object,
					   String member) throws IOException {
		try{
			try {
				Bolg bolg = registered(object);
				Object o = bolg.get(member);
				sendAnswer(request,o);
			} catch(NoSuchFieldException nsfe) {
				System.out.println("No field in get.");
				sendError(request, new GloopException("No such field: "+member,nsfe));
			}
		} catch(IOException ioe) {
			throw new ConnectionLost(ioe);
		}
	}
	
	public void gotName(Integer request,
						String name) throws IOException {
		Bolg bolg = bound(name);
	}

	public void gotAnswer(Integer request,
						  Object value)
		throws IOException {
		answers.put(request,value==null?"__NULL__":value);
	}
	
	public void gotError(Integer request,
						 String error,
						 String traceback) 
		throws IOException, GloopException {
		throw new GloopException(error,traceback);
	}

	public void snarf(Vector v) throws IOException {
		switch(((Integer)v.elementAt(0)).intValue()) {
		case SET:
			gotSet((Integer)v.elementAt(1),
				   (Integer)v.elementAt(2),
				   (String)v.elementAt(3),
				   v.elementAt(4));
			break;
		case GET:
			gotGet((Integer)v.elementAt(1),
				   (Integer)v.elementAt(2),
				   (String)v.elementAt(3));
			break;
		case CALL:
			Object[] ob=new Object[v.size()-3];
			for (int i = 0; i < v.size()-3; i++)
			{
				ob[i]=v.elementAt(i++);
			}
			gotCall((Integer)v.elementAt(1),
					(Integer)v.elementAt(2),
					ob);
			break;
		case ANSWER:
			gotAnswer((Integer)v.elementAt(1),
					  v.elementAt(2));
			break;
		case ERROR:
			gotError((Integer)v.elementAt(1),
					 (String) v.elementAt(2),
					 (String) v.elementAt(3));
			break;
		case FORGET:
			gotForget((Integer)v.elementAt(1));
		case NAME:
			gotName((Integer)v.elementAt(1),
					(String)v.elementAt(2));
			break;
		}
	}
}
