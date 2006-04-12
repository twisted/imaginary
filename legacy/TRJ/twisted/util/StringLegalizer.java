package twisted.util;

import java.util.Enumeration;
import java.io.*;

/**
 * This class will legalize a string, so it can be outputted to a file
 * as a single quoted string.  It does things like turning returns
 * into '\n's, tabs into '\t's, etc.
 *
 * @version 1.0, 28 Mar 1999
 * @author Glyph Lefkowitz
 */

public class StringLegalizer
{
	static boolean STRICT=false;

	public static String delegalize(String s)
	{
		if(s==null) return "null";
		StringEnumerator e = new StringEnumerator(s);
		StringBuffer t = new StringBuffer();
		while(e.hasMoreElements())
		{
			char c = e.nextChar();
			if (c=='\\')
			{
				c=e.nextChar();
				switch (c)
				{
				case 'n':
					t.append("\n");
					break;
					/*  
						case ' ':
						if(STRICT) t.append("\\ ");
						break;
						case '*':
						if(STRICT) t.append("\\*");
						break;
					*/
				case 't':
					t.append("\t");
					break;
					
				case 'r':
					t.append("\r");
					break;
					
				default:
					t.append(c);
					break;
				}
			}
			else
				t.append(c);
		}
		return t.toString();
	}
	
	/**
	 * Perform the legalization on the provided string.
	 *
	 * @param s The string to legalize.
	 *
	 * @return The legalized string.
	 */
	
	public static String legalize(String s)
	{
		if(s==null) return "null";
		StringEnumerator e = new StringEnumerator(s);
		StringBuffer t = new StringBuffer();
		while(e.hasMoreElements())
		{
			char c = e.nextChar();
			switch (c)
			{
			case '\n':
				t.append("\\n");
				break;
				/*  
					case ' ':
					if(STRICT) t.append("\\ ");
					break;
					case '*':
					if(STRICT) t.append("\\*");
					break;
				*/
			case '\"':
				t.append("\\\"");
				break;
				
			case '\t':
				t.append("\\t");
				break;
				
			case '\r':
				t.append("\\r");
				break;
				
			case '\\':
				t.append("\\\\");
				break;
				
			default:
				t.append(c);
				break;
			}
		}
		return t.toString();
	}
}
