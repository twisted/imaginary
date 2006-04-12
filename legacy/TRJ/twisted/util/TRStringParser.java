package twisted.util;

import java.util.Enumeration;
import java.util.NoSuchElementException;

public class TRStringParser implements Enumeration {
	private int currentPosition;
	private int maxPosition;
	private String str;
	
	boolean tokenQuoted;
	
	public TRStringParser(String str) {
		currentPosition = 0;
		this.str = str;
		maxPosition = str.length();
	}

	/**
	 * Tests if there are more tokens available from this tokenizer's string.
	 *
	 * @return	<code>true</code> if there are more tokens available from this
	 *			tokenizer's string; <code>false</code> otherwise.
	 */
	public boolean hasMoreTokens() {
		if(currentPosition >= maxPosition) return false;
		while (Character.isWhitespace(str.charAt(currentPosition)))
			if(++currentPosition >= maxPosition)
			{
				currentPosition = maxPosition - 1;
				return false;
			}
		return true;
	}
	
	/**
	 * Returns the next token from this string tokenizer.
	 *
	 * @return	   the next token from this string tokenizer, or null
	 *			   if there are no elements left
	 */
	public String nextToken() throws NoSuchElementException
	{
		tokenQuoted = false;
		boolean escape = false;
		if(currentPosition >= maxPosition) throw new NoSuchElementException();
		while (Character.isWhitespace(str.charAt(currentPosition)))
			if(++currentPosition >= maxPosition)
			{
				currentPosition = maxPosition - 1;
				throw new NoSuchElementException();
			}
		
		char cur = str.charAt(currentPosition);
		if (cur == '"')
		{
			tokenQuoted = true;
			currentPosition++;
		}
		
		int startPosition = currentPosition;
		while (currentPosition < maxPosition)
		{
			cur = str.charAt(currentPosition);
			if (!escape && (tokenQuoted?
					cur == '"' :
					Character.isWhitespace(cur)))
			{
				currentPosition++;
				return unFuxor(str.substring(startPosition, currentPosition - 1));
			}
				;
			if(cur == '\\')
				escape = !escape;
			else
				escape = false;
			
			currentPosition++;
		}
		return unFuxor(str.substring(startPosition, currentPosition));
	}
	
	/**
	 * Returns if the last token returned was contained in quotation marks
	 */
	public boolean wasQuoted()
	{
		return tokenQuoted;
	}
	
	public static String unFuxor(String in)
	{
		int max = in.length();
		StringBuffer out = new StringBuffer(in.length());
		int cur = 0;
		try
		{
		while(true)
		{
			int pos = in.indexOf('\\', cur);
			if (pos == -1)
				break;
			out.append(in.substring(cur, pos));
			cur = pos+1;
			char c = in.charAt(cur++);
			switch(c)
			{
				case 'n': out.append('\n'); break;
				case 't': out.append('\t'); break;
				case 'r': out.append('\r'); break;
				case 'u': //unicode escape sequence
				decode_unicode: {
					int val = 0;
					for(int i = 0; i < 4; i++)
					{
						c = Character.toLowerCase(in.charAt(cur++));
						if(c >= '0' && c <= '9')
							val = val*16 + c - '0';
						else if(c >= 'a' && c <= 'f')
							val = val*16 + c - 'a' + 10;
						else
							break decode_unicode;
					}
					out.append((char)val);
				}
				break;
				default:
					out.append(c);
				break;
			}
		}
		out.append(in.substring(cur));
		} catch (StringIndexOutOfBoundsException e) {e.printStackTrace(); }
		return out.toString();
	}

	/**
	 * Returns the same value as the <code>hasMoreTokens</code>
	 * method. It exists so that this class can implement the
	 * <code>Enumeration</code> interface. 
	 *
	 * @return	<code>true</code> if there are more tokens;
	 *			<code>false</code> otherwise.
	 * @see		java.util.Enumeration
	 * @see		java.util.StringTokenizer#hasMoreTokens()
	 */
	public boolean hasMoreElements() {
		return hasMoreTokens();
	}

	/**
	 * Returns the same value as the <code>nextToken</code> method,
	 * except that its declared return value is <code>Object</code> rather than
	 * <code>String</code>. It exists so that this class can implement the
	 * <code>Enumeration</code> interface. 
	 *
	 * @return	   the next token in the string.
	 * @exception  NoSuchElementException  if there are no more tokens in this
	 *				 tokenizer's string.
	 * @see		   java.util.Enumeration
	 * @see		   java.util.StringTokenizer#nextToken()
	 */
	public Object nextElement() {
		return nextToken();
	}
}
