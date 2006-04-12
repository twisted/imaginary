package twisted.util.awt;

import java.awt.Panel;
import java.awt.Image;
import java.awt.Graphics;

import twisted.util.swing.*;

public class TilePanel extends Panel
{
	public TilePanel(String imgname)
	{
		setImage(imgname);
	}
	
	final void tileImage(Image a, Graphics b)
	{
		int wdth=a.getWidth(this);
		int hght=a.getHeight(this);
		if((wdth>0) && (hght>0))
			for(int i = -1;i<getBounds().width;i+=wdth)
			{
				for(int j = -1; j<getBounds().height;j+=hght)
				{
					b.drawImage(a,i,j,this);
				}
			}
	}
	
	Image bg;
	
	public synchronized void setImage(Image a)
	{
		bg=a;
		// textchanged=true;
		repaint();
	}
	
	public void setImage(String s)
	{
		setImage(ImageServer.getImage(s,this));
	}
	
	public void update(Graphics g)
	{
		tileImage(bg,g);
		super.update(g);
	}
}
