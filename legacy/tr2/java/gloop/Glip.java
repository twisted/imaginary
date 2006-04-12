package gloop;

import java.io.InputStream;
import java.io.OutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;

import java.util.Vector;
import java.util.Enumeration;

import java.net.Socket;

public class Glip
{
	public static final byte LIST=0;
	public static final byte STRING=1;
	public static final byte INT=2;
	public static final byte BYTE=3;
	public static final byte SHORT=4;
	public static final byte REFERENCE=5;
	public static final byte VOID=6;
	
	private DataOutputStream os;
	private DataInputStream is;
	
	public Glip()
	{
	}

	public void setInputStream(InputStream iis) {
		is=new DataInputStream(iis);
	}
	
	public void setOutputStream(OutputStream ios) {
		os=new DataOutputStream(ios);
	}

	public void writeByte(byte b) throws IOException {
		os.writeByte(b);
	}
	
	public void writeShort(int b) throws IOException {
		os.writeShort(b);
	}

	public void writeInt(int b) throws IOException {
		os.writeInt(b);
	}

	public void writeString(String s) throws IOException {
		os.writeUTF(s);
	}
	
	public void writeList(Vector v) throws IOException {
		writeShort(v.size());
		Enumeration e = v.elements();
		while(e.hasMoreElements()) {
			Object o = e.nextElement();
			write(o);
		}
	}

	public void writeList(Object[] a) throws IOException {
		writeShort(a.length);
		for (int i = 0; i<a.length; i++)
			write(a[i]);
	}

	public void writeReference(Object o) throws IOException {
		System.out.println("glip can't write a reference.");
		writeInt(0);
	}
	
	public void write(Object o) throws IOException {
		if (o instanceof Integer) {
			writeByte(INT);
			writeInt(((Integer)o).intValue());
		} else if (o instanceof String) {
			writeByte(STRING);
			writeString((String) o);
		} else if (o instanceof Byte) {
			writeByte(BYTE);
			writeByte(((Byte)o).byteValue());
		} else if (o instanceof Vector) {
			writeByte(LIST);
			writeList((Vector)o);
		} else if (o instanceof Object[]) {
			writeList((Object[])o);
		} else {
			writeByte(REFERENCE);
			writeReference(o);
		}
	}
	
	public int readByte() throws IOException {
		return is.readUnsignedByte();
	}

	public int readShort() throws IOException {
		return is.readUnsignedShort();
	}
	
	public int readInt() throws IOException {
		return is.readInt();
	}
	
	public String readString() throws IOException {
		return is.readUTF();
	}
	
	public Vector readList() throws IOException {
		Vector v = new Vector();
		int x = readShort();
		v.setSize(x);
		for (int i=0;i<x;i++) {
			v.setElementAt(read(),i);
		}
		return v;
	}
	
	public Object readReference() throws IOException {
		System.out.println("GLIP READREFERENCE");
		return null;
	}
	
	public Object read() throws IOException {
		byte type = is.readByte();
		switch(type) {
		case LIST:
			return readList();
		case STRING:
			return readString();
		case BYTE:
			return new Integer(readByte());
		case INT:
			return new Integer(readInt());
		case SHORT:
			return new Integer(readShort());
		case REFERENCE:
			return readReference();
		case VOID:
			return null;
		}
		return null;
	}
	
	public static void main(String[] args) throws Exception {
		Socket skt = new Socket("localhost",8989);
		Glip glip = new Glip();
		glip.setInputStream(skt.getInputStream());
		glip.setOutputStream(skt.getOutputStream());
		Vector j = new Vector();
		j.addElement("tanstaafl");
		j.addElement("taaan");
		Vector v = new Vector();
		v.addElement("a");
		v.addElement(new Integer(7));
		v.addElement(j);
		glip.write(v);
	}
}
