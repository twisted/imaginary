package twisted.util.swing;

import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.URL;
import java.util.*;

import javax.swing.text.*;
import javax.swing.event.*;
import javax.swing.*;

public class BackgroundThingy extends JPanel
{
	public BackgroundThingy()
	{
		super();
	}
	
	public void paintComponent(Graphics g)
	{
		if(bg != null)
			tileImage(bg,g);
		else
			g.clearRect(0,0,getBounds().width, getBounds().height);
	}
	protected Image bg;
	public void setImage(String s)
	{
		setImage(ImageServer.getImage(s,this));
	}
	int wdth;
	int hght;
	public void setImage(Image a)
	{
		bg=a;
		//	textchanged=true;
		repaint();
	}
	
//	What's the point of this code? Making it always return (0,0) seems to make no diff... (JYK)

	// This is so the image will tile seamlessly between panels.  (glyph)
	
	private Point getFLocation()
	{
		if (!isShowing())
			return new Point(0,0);
		Point p = getLocationOnScreen();
		Container q=getParent();
		while( !( q instanceof Window ))
		{
			q=q.getParent();
		}
		
		Point r = q.getLocationOnScreen();
		p.x-=r.x;
		p.y-=r.y;
		return p;
	}
	
	final void tileImage(Image a, Graphics b)
	{
		wdth=a.getWidth(this);
		hght=a.getHeight(this);
		Point p = getFLocation();
		
		if((wdth>0) && (hght>0))
			for(int i = -(p.x%wdth);i<getBounds().width;i+=wdth)
			{
				for(int j = -(p.y%hght); j<getBounds().height;j+=hght)
				{
					b.drawImage(a,i,j,this); 
				}
			}
	}
}
