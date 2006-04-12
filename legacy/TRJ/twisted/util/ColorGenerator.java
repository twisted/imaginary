package twisted.util;

import java.awt.Color;
import java.util.StringTokenizer;

public class ColorGenerator
{
	public static Color createColor(String s)
	{
		StringTokenizer st = new StringTokenizer(s);
		
		String red = st.nextToken();
		String green = st.nextToken();
		String blue = st.nextToken();
		
		return new Color(Integer.parseInt(red),Integer.parseInt(green),Integer.parseInt(blue));
	}
}
