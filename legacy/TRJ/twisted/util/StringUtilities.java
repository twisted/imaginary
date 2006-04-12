package twisted.util;

import java.util.Stack;
import java.util.Vector;

/**
 *  This class contains several convenient methods useful
 *  when dealing with strings.
 *
 *  @author Phil Christensen
 *  @version 1.0, 7/20/99
 */
public class StringUtilities
{
	/**
	 *  Takes a given String and splits in into an array of strings based
	 *  	on an arbitrary delimiter.
	 *  	Modelled after perl's split function.
	 *  
	 *  @param text String to split
	 *  @param delimiter String to split around
	 *  @return array of tokens in string
	 */
	public static String[] split(String text, String delimiter)
	{
		if(text.equals("")) return new String[0];
		if(delimiter.equals(""))
		{
			String[] result = new String[text.length()];
			for(int i = 0; i < result.length; i++)
				result[i] = text.charAt(i) + "";
			return result;
		}

		int temp = 0, i = 0;
		int tokenBegin = 0;
		
		
		for(i = 0; i < text.length(); i++)
		{
			if(text.substring(i, i + delimiter.length()).equals(delimiter))
			{
				temp++;
				tokenBegin = i + delimiter.length();
				i = tokenBegin - 1;
			}
		}

		String[] result = new String[++temp];
		tokenBegin = 0;
		for(i = 0, temp = 0; i <= text.length() - delimiter.length(); i++)
		{
			if(text.substring(i, i + delimiter.length()).equals(delimiter))
			{
				String token = text.substring(tokenBegin, tokenBegin + (i - tokenBegin));
				result[temp++] = token;
				tokenBegin = i + delimiter.length();
				i = tokenBegin - 1;
			}
		}

		if(tokenBegin < text.length())
			result[temp] = text.substring(tokenBegin);
		return result;
	}

	/**
	 *  Takes an array of Objects and concatanates them around a delimiter.
	 *  	Modelled after perl's join function.
	 *
	 *  @param array Object[] of things to join.
	 *  @param delimiter String to separate fields, if any.
	 */
	public static String join(Object[] array, String delimiter)
	{
		String result = "";
		for(int i = 0; i < array.length; i++)
		{
			result += array[i].toString();
			if(i != array.length - 1)
				result += delimiter;
		}
		return result;
	}

	/**
	 *  Replaces an arbitrary string of text with another arbitrary String.
	 *  	Can optionally replace all ocurrences or just the first, or any
	 * 	 occurences after a certain index.
	 *
	 *  @param text String to search
	 *  @param sought String to look for
	 *  @param substitute String to replace with
	 *  @param start index to start at
	 *  @param global whether to continue past the first match.
	 *  @return String new String with replacements.
	*/
	public static String replaceInString(String text, String sought, String substitute, int start, boolean global)
	{
		for(int i = start; i <= text.length() - sought.length(); i++)
		{
			if(text.substring(i, i + sought.length()).equals(sought))
			{
				text = text.substring(0, i) + substitute + text.substring(i + sought.length());
				i = i + substitute.length() - 1;
			}
		}
		return text;
	}

	/**
	 *  Replaces all occurrances of an arbitrary string of text with
	 * 	 another arbitrary String.
	 *
	 *  @param text String to search
	 *  @param sought String to look for
	 *  @param substitute String to replace with
	 *  @return String new String with replacements.
	*/	
	public static String replaceInString(String text, String sought, String substitute)
	{
		return replaceInString(text, sought, substitute, 0, true);
	}

	/**
	 *  Replaces an arbitrary string of text with another arbitrary String.
	 *
	 *  @param text String to search
	 *  @param sought String to look for
	 *  @param substitute String to replace with
	 *  @param global whether to continue past the first match.
	 *  @return String new String with replacements.
	*/
	public static String replaceInString(String text, String sought, String substitute, boolean global)
	{
		return replaceInString(text, sought, substitute, 0, global);
	}

	/**
	 *  Replaces all occurances of an arbitrary string of text with
	 *	another arbitrary String, starting at a particular position.
	 *
	 *  @param text String to search
	 *  @param sought String to look for
	 *  @param substitute String to replace with
	 *  @param start index to start at
	 *  @return String new String with replacements.
	*/
	public static String replaceInString(String text, String sought, String substitute, int start)
	{
		return replaceInString(text, sought, substitute, start, true);
	}
	
	/**
	 *  Replaces all occurances of an Object in an array with
	 *	another arbitrary Object.
	 *
	 *  @param array Object[] to search
	 *  @param sought Object to look for
	 *  @param substitute Object to replace with
	 *  @return Object[] new Object[] with replacements.
	*/
	public static Object[] replaceInArray(Object[] array, Object sought, Object substitute)
	{
		Object[] result;
		if(! (array instanceof Object[]))
		{
			result = new Object[array.length];
			System.arraycopy(array, 0, result, 0, array.length);
		}
		else
		{
			result = array;
		}
		for(int i = 0; i < result.length; i++)
			if(result[i].equals(sought))
				result[i] = substitute;
		return result;
	}
	
	/**
	 *  Replaces all occurances of an arbitrary string of text with
	 *	an arbitrary Object, and returns an Object[] of the words in
	 *	the sentence.
	 *
	 *  @param sentence String to search
	 *  @param variables String[] of variables to look for.
	 *  @param subs Object[] to insert into final array
	 *  @return Object[] new Object[] with replacements.
	*/
	public static Object[] substituteVariables(String sentence, String[] variables, Object[] subs)
	{
		String[] temp = StringUtilities.split(sentence, " ");
		Object[] words = new Object[temp.length];
		System.arraycopy(temp, 0, words, 0, temp.length);
		for(int i = 0; i < variables.length; i++)
		{
			words = replaceInArray(words, variables[i], subs[i]);
		}
			
		for(int j = 0; j < words.length; j++)
		{
			if(j > 0 && !(words[j-1] instanceof String))
				words[j] = " " + words[j];
			if(j != words.length - 1)
				words[j] = words[j] + " ";
		}
		return words;
	}
	
	/**
	 * Pads the input string with spaces to make it the right number of characters
	 * long.
	 */
	public static String pad(String in, int chars)
	{
		int count = in.length();
		if(chars <= count) return in;
		
		StringBuffer b=new StringBuffer(chars);
		b.append(in);
		for(; count < chars; count++)
		{
			b.append(' ');
		}
		return b.toString();
	}
}
