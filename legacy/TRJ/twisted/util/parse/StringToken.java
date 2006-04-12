package twisted.util.parse;

import java.util.StringTokenizer;
import java.util.Hashtable;

public class StringToken implements Token
{
	public static final int ST_END=-1;
	public static final int ST_WORD=0;
	public static final int ST_QUOTE=1;
	public static final int ST_PREP=2;
	public static final int ST_TERM=4;
	
	private int strtype;
	
	public int type()
	{
		return strtype;
	}
	
	StringTokenizer st;
	String str;
	
	public Object data(){return str;}
	
	public StringToken(String s)
	{
		// I SAID, PAY NO ATTENTION TO THE MAN BEHIND THE CURTAIN!
		// (i'm cheating)
		
		st=new StringTokenizer(s,"\r\n\t \"",true);
	}
	
	StringToken next;
	
	public Token next()
	{
		if(next == null)
		new StringToken(st,this);
		
		return next;
	}
	
	//this goes somewhere, not sure where yet tho

	static Hashtable preps;
	static Hashtable abs;
	static Hashtable whitespace;
	static
	{
		preps=new Hashtable();
		whitespace=new Hashtable();

		preps.put("with","with");
		preps.put("using","using");

		preps.put("into","into");
		preps.put("in","in");
		preps.put("on","on");
		// preps.put("off","off");
		preps.put("to","to");
		preps.put("at","at");
		preps.put("from","from");
		
		whitespace.put(" "," ");
		whitespace.put("\r","\r");
		whitespace.put("\t","\t");
		whitespace.put("\n","\n");
		
	}
	
	protected StringToken(StringTokenizer thest,StringToken prev)
	{
		st=thest;
		prev.next=this;
				
		String tok = null;
		if(st.hasMoreTokens())
		{
			tok=st.nextToken();
			System.out.println("("+tok+")");
			if(whitespace.containsKey(tok))
			{
				strtype=-2;
				System.out.println("Whitespace Ignored...");
				str="BAD DATA";
				new StringToken(st,prev);
			}
			else if(preps.containsKey(tok))
			{
				strtype=ST_PREP;
			}
			else if(tok.equals("\"")||tok.equals("'"))
			{
				strtype=ST_QUOTE;
			}
			else if(tok.equals(".")||tok.equals(";"))
			{
				strtype=ST_TERM;
			}
			else
			{
				strtype=ST_WORD;
			}
			str=tok;
		}
		else
		{
			strtype=ST_END;
		}
		System.out.println(strtype);
		//str="blech";
	}
	
}
