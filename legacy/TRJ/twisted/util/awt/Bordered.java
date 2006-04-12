package twisted.util.awt;

import java.awt.*;
import java.util.Vector;
import java.util.Enumeration;

class Borderline extends Canvas
{
	Dimension x;
	
	static Vector phu=new Vector();
	
	public static void repaintall()
	{
		Enumeration e = phu.elements();
		while(e.hasMoreElements())
		{
			Borderline b = (Borderline) e.nextElement();
			b.repaint();
		}
	}
	
	private void addthis()
	{
		phu.addElement(this);
	}
	
	public static Color lighter(Color c) {
		return new Color
			(
				c.getRed()+ ((255-c.getRed())/2), 
				c.getGreen()+ ((255-c.getGreen())/2),
				c.getBlue() + ((255-c.getBlue())/2)
				);
	}
	
	public static Color darker(Color c)
	{
		return new Color
			(
				c.getRed()/2,
				c.getGreen()/2,
				c.getBlue()/2
				);
		
	}
	
	public static Color currcolor=Color.black;
	
	public Borderline()
	{
		x=new Dimension(6,6);
		addthis();
	}
	
	public void update(Graphics g)
	{
		paint(g);
	}
	
	public void paint(Graphics g)
	{
		int w=getBounds().width;
		int h=getBounds().height;
		
		g.setColor(currcolor);
		g.fillRect(0,0,w,h);
		h--;
		h--;
		w--;
		w--;
		g.setColor(lighter(currcolor));
		g.fillRect(1,1,w,h);
		w--;
		w--;
		h--;
		h--;
		g.setColor(lighter(lighter(currcolor)));
		g.fillRect(2,2,w,h);
		/*
		  g.setColor(Color.darkGray);
		  g.fillRect(0,0,w--,h--);
		  g.setColor(Color.gray);
		  g.fillRect(1,1,w--,h--);
		  g.setColor(Color.lightGray);
		  g.fillRect(2,2,w,h);*/
		
	}
	
	public Dimension getPreferredSize()
	{
		return x;
	}
	public Dimension getMinimumSize()
	{
		return x;
	}
}

public class Bordered extends Panel
{	 
	public static Color lighter(Color c)
	{
		return new Color
			(
				max(8*(1+c.getRed())/7,255), 
				max(8*(1+c.getGreen())/7,255),
				max(8*(1+c.getBlue())/7,255)
				);
	}
	
	private static int max(int a, int b)
	{
		return
			a<b?a
			:b
			;
	}
	
	public static Color darker(Color c)
	{
		return new Color
			(
				max(7*c.getRed()/8,255),
				max(7*c.getGreen()/8,255),
				max(7*c.getBlue()/8,255)
				);
		
	}
	public static void setColor(Color c)
	{
		Borderline.currcolor=c;
		Borderline.repaintall();
	}
	public Bordered(Component c,String s)
	{
		setLayout(new BorderLayout());
		add("Center",c);
		if(s.equals("all"))
		{
			add("North",new Borderline());
			add("South",new Borderline());
			add("East",new Borderline());
			add("West",new Borderline());
		} else add(s,new Borderline());
	}
}
