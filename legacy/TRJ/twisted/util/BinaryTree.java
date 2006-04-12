package twisted.util;

import java.util.Dictionary;
import java.util.Hashtable;
import java.util.Enumeration;

public class BinaryTree extends Dictionary
{
	class BinaryConflict
	{
		public BinaryConflict(Object key, Object data)
		{
			this.key=key;
			this.data=data;
		}
		Object key;
		Object data;
		BinaryConflict bc;
	}
	
	class BinaryNode extends BinaryConflict
	{
		BinaryNode(Object key, Object data, int hcode)
		{
			super(key,data);
			this.hcode=hcode;
		}
		BinaryNode(Object key, Object data, int hcode, BinaryNode a, BinaryNode b)
		{
			this(key,data,hcode);
			this.a=a;
			this.b=b;
		}
		BinaryNode a;
		BinaryNode b;
		int hcode;
	}
	static final int KEYS=0;
	static final int ELEMENTS=1;
	
	class BinaryEnumeration implements Enumeration
	{
		Object elementBuffer;
		int kd;
		public BinaryEnumeration(BinaryNode t, int keyd)
		{
			bn = t;
			kd=keyd;
			if(t.a!=null) mea=new BinaryEnumeration(t.a,kd);
			if(t.b!=null) meb=new BinaryEnumeration(t.b,kd);
		}
		
		public BinaryNode bn;
		public BinaryConflict bc;
		
		public Enumeration mea;
		public Enumeration meb;

		void cacheElement()
		{
			if (elementBuffer == null) if (mea != null) if(mea.hasMoreElements())
			{
				elementBuffer=mea.nextElement();
			} else mea=null;
			
			if (elementBuffer == null) if (meb != null) if(meb.hasMoreElements())
			{
				elementBuffer=meb.nextElement();
			} else meb=null;
			
			if (elementBuffer == null) if (bn!=null)
			{
				if (kd==KEYS) 
					elementBuffer=bn.key;
				else
					elementBuffer=bn.data;
				bc=bn.bc;
				bn=null;
			}
			
			if(elementBuffer == null) if (bc!=null)
			{
				while(bc!=null)
				{
					if(kd==KEYS)
						elementBuffer=bc.key;
					else
						elementBuffer=bc.data;
					bc=bc.bc;
					if (elementBuffer!=null)break;
				}
			}
		}
		
		public boolean hasMoreElements()
		{
			cacheElement();
			return (elementBuffer!=null);
		}
		public Object nextElement()
		{
			cacheElement();
			Object q = elementBuffer;
			elementBuffer=null;

			return q;
		}
	}
	
	BinaryNode bn;
	int elementCount;
	
	public BinaryTree()
	{
		elementCount=0;
	}
	
	public boolean isEmpty()
	{
		return (bn==null);
	}
	
	public int size()
	{
		return elementCount;
	}
	
	public synchronized Enumeration elements()
	{
		return new BinaryEnumeration(bn,ELEMENTS);
	}
	public synchronized Enumeration keys()
	{
		return new BinaryEnumeration(bn,KEYS);
	}

	
	public synchronized Object put(Object key, Object data)
	{
		elementCount++;
		BinaryNode n = bn;
		int hcode = key.hashCode();
		if (bn==null)
		{
			bn=new BinaryNode(key,data,hcode);
			return null;
		}
		while(true)
		{
			if (n.hcode==hcode)
			{
				BinaryConflict bc=n;
				BinaryConflict bne=null;
				while (bc != null)
				{
					if(bc.key.equals(key))
					{
						Object r = bc.data;
						bc.data=data;
						return r;
					}
					bne=bc;
					bc=bc.bc;
				}
				bne.bc=new BinaryConflict(key,data);
				return null;
			}
			else if (n.hcode < hcode)
			{
				if (n.a==null)
				{
					n.a=new BinaryNode(key,data,hcode);
					return null;
				}
				else 
				{
					n=n.a;
					continue;
				}
			}
			else if (n.hcode > hcode)
			{
				if (n.b==null)
				{
					n.b=new BinaryNode(key,data,hcode);
					
					return null;
				}
				else 
				{
					n=n.b;
					continue;
				}
			}
		}
		//return null;
	}
	
	// this doesn't work yet
	
	public synchronized Object remove(Object key)
	{
		elementCount--;
		BinaryNode n = bn;
		BinaryNode parentn = null;
		BinaryConflict parentc = null;
		char abc = 'x';
		int hcode = key.hashCode();
		if (bn==null)
		{
			return null;
		}
		while(true)
		{
			if (n.hcode==hcode)
			{
				BinaryConflict bc=n;
				while (bc != null)
				{
					if(bc.key.equals(key))
					{
						Object o = bc.data;
						if(bc instanceof BinaryNode)
						{
							if(n.a != null || n.b != null) return o;
						}
						switch(abc)
						{
						case 'a':
							parentn.a=null;
							break;
						case 'b':
							parentn.b=null;
							break;
						case 'c':
							parentc.bc=bc.bc;
							break;
						case 'x':
							if (parentc != null)
							{
								System.err.println("BinaryTree impl broken (this should NEVER happen)");
							}
							else
							{
								bn=null;
							}
							break;
						default:
							System.err.println("Alpha particle corruption in memory...");
						}
						return o;
					}
					if(bc.data!=null || 
					   ( 
						(bc.bc != null) ? (bc.bc.bc == null) : true 
						)
					   )
					{
						parentc=bc;
						abc='c';
					}
					bc=bc.bc;
				}
				return null;
			}
			else if (n.hcode < hcode)
			{
				if (n.a==null)
				{
					return null;
				}
				else 
				{
					if(n.b!=null || n.bc!=null)
					{
						parentc=n;
					}
					n=n.a;
					continue;
				}
			}
			else if (n.hcode > hcode)
			{
				if (n.b==null)
				{
					return null;
				}
				else 
				{
					if(n.a!=null || n.bc!=null)
					{
						parentc=n;
					}
					n=n.b;
					continue;
				}
			}
		}
	}
	
	public synchronized Object get(Object key)
	{
		BinaryNode n = bn;
		int hcode = key.hashCode();
		if (bn==null)
		{
			return null;
		}
		while(true)
		{
			if (n.hcode==hcode)
			{
				BinaryConflict bc=n;
				while (bc != null)
				{
					if(bc.key.equals(key))
					{
						return bc.data;
					}
					bc=bc.bc;
				}
				return null;
			}
			else if (n.hcode < hcode)
			{
				if (n.a==null)
				{
					return null;
				}
				else 
				{
					n=n.a;
					continue;
				}
			}
			else if (n.hcode > hcode)
			{
				if (n.b==null)
				{
					return null;
				}
				else 
				{
					n=n.b;
					continue;
				}
			}
		}
	}

	public static void lltest(Dictionary d)
	{
		System.out.println("Put: null null null there silly you null null null");
		System.out.println(d.put("hello","there"));
		System.out.println(d.put("you","silly"));
		System.out.println(d.put("person","you"));
		System.out.println(d.put("hello","there"));
		System.out.println(d.put("you","silly"));
		System.out.println(d.put("person","you"));
		System.out.println(d.put("hello","there"));
		System.out.println(d.put("you","silly"));
		System.out.println(d.put("person","you"));
		System.out.println(d.put("HELLO","there"));
		System.out.println(d.put("YOU","silly"));
		System.out.println(d.put("PERSON","you"));

		System.out.println("Get: there silly you");
		System.out.println(d.get("hello"));
		System.out.println(d.get("you"));
		System.out.println(d.get("person"));
		System.out.println("Enumerate: there silly you, no particular order");
		Enumeration e = d.elements();
		while(e.hasMoreElements())
		{
			System.out.println(e.nextElement());
		}
		System.out.println("Remove: again");
		System.out.println(d.remove("hello"));
		System.out.println(d.remove("you"));
		System.out.println(d.remove("person"));
		System.out.println("Empty: true");
		System.out.println(d.isEmpty());
	}
	
	public static void main(String[] args)
	{
		System.out.println("---HashTable---");
		lltest(new Hashtable());
		System.out.println("---LinkedList---");
		lltest(new LinkedList());
		System.out.println("---BinaryTree---");
		lltest(new BinaryTree());
	}
}
