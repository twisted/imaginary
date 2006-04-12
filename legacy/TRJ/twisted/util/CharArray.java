package twisted.util;

/**
 * Performs a number of useful functions on character arrays.
 *
 * @version 0.99.1, 15 Jun 1998
 * @author Glyph Lefkowitz
 */

public class CharArray
{
	/**
	* Copies an array into a newer array of double the length.
	   *
	   * @return An array of twice the length of the specified one.
	   * @param x The array to double and copy. 
	   */
	public static final char[] rebuf(char[] x)
	{
		char[] newer = new char[x.length*2];
		System.arraycopy (x,0,newer,0,x.length);
		return newer;
	}
	/**
	   * Inserts a character into an array.	 This method may or may
	   * not use the original array depending upon the length.
	   *
	   * @return An array with the specified character inserted.
	   *
	   * @param x The array to insert into.
	   *
	   * @param y The character to insert.
	   *
	   * @param at The position to insert at.
	   *
	   * @param len The length of the contents of the array.  Specify
	   * the length of the non-throwaway material present in your
	   * array here so this method knows when to re-buffer the data.
	   */
	
	public static final char[] insert(char[] x, char y, int at, int len)
	{
		char[] rval;
		if(x.length<len+1)
		{
			rval=rebuf(x);
			//System.out.println("REbuff");
		}
		else
		{
			rval=x;
		}
		System.arraycopy (rval,at,rval,at+1,len-at);
		rval[at]=y;
		return rval;
	}
	/**
	   * Removes a single character from the specified array at the
	   * specified location.
	   *
	   * @param x The array to alter.
	   *
	   * @param at The index to remove the character from.
	   *
	   * @param len The length of the non-throwaway contents of the array.
	   *
	   * @return The incoming variable 'x'.
	   */
	public static final char[] remove(char[] x,int at, int len)
	{
		System.arraycopy(x,at,x,at-1,len-at);
		return x;
	}
	/**
	   * Duplicates a character array.
	   *
	   * @param a The array to copy.
	   *
	   * @return An exact copy of a, at a different spot in memory.
	   */
	public static final char[] dup(char[] a)
	{
		char[] r = new char[a.length];
		System.arraycopy(a,0,r,0,a.length);
		return r;
	}
	
	/**
	   * Returns a subarray from a starting point to an ending point.
	   *
	   * @param a The array to split.
	   *
	   * @param start The starting point of the subarray.
	   *
	   * @param fin The finishing point of the subarray.
	   * 
	   * @return The subarray.
	   */
	public static final char[] sub(char[] a, int start, int fin)
	{
		char[] r = new char[fin-start];
		System.arraycopy(a,start,r,0,fin-start);
		return r;
	}

	/**
	   * Concatenates two arrays and returns the result.
	   * 
	   * @param a The first array.
	   * 
	   * @param b The second array.
	   *
	   * @return An array that is equivalent to { a[0],
	   * a[1]... a[a.length-1], b[0], b[1]... b[b.length-1] };
	   */
	public static final char[] cat(char[] a, char[] b)
	{
		if(b==null) return dup(a);
		if(a==null) return dup(b);
		char[] c = new char[a.length+b.length];
		System.arraycopy(a,0,c,0,a.length);
		System.arraycopy(b,0,c,a.length,b.length);
		return c;
	}
	/**
	   * Concatenates two non-garbage segments of two arrays.
	   *
	   * @param a The first array.
	   *
	   * @param b The second array.
	   * 
	   * @param lena The length of the contents of a.
	   *
	   * @param lenb The length of the contents of b.
	   *
	   * @return An array equivalent to { a[0], a[1]... a[lena-1],
	   * b[0], b[1]... b[lenb]};
	   */
	public static final char[] cat(char[] a,int lena, char[] b, int lenb)
	{
		if(b==null) return dup(a);
		if(a==null) return dup(b);
		
		char[] c = new char[lena+lenb];
		System.arraycopy(a,0,c,0,lena);
		System.arraycopy(b,0,c,lena,lenb);
		return c;
	}
}
