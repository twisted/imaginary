package twisted.util.awt;
import twisted.util.*;
import java.awt.*;
import java.util.*;
import java.awt.image.*;
import twisted.util.swing.*;

public class ScrolltextThingy extends Canvas
{
	public ScrolltextThingy(int a, int b)
	{
		x=new Dimension(a,b);
		textchanged=true;
		BIG=new Font("Courier",Font.BOLD,12);
		LITTLE=new Font("Courier",Font.PLAIN,12);
		thel = new LinkedList();
		setColor(Color.white);
		//setBackground(Color.black);
	}
	
	public Font BIG;
	public Font LITTLE;
	Dimension x;
	LinkedList thel;
	public Dimension getPreferredSize()
	{
		return x;
	}
	
	public void clearText()
	{
		thel=new LinkedList();
	}
	
	public void appendText(String nbuf)
	{
		thel.addElement(nbuf);
		textchanged=true;
		repaint();
	}
	
	public String getText()
	{
		String s = new String();
		String tlm;
		for(Enumeration e = thel.elements();e.hasMoreElements();)
		{
			tlm=((String) e.nextElement());
			
			s = tlm+s;
		}
		return s;
	}
	
	private boolean textchanged;
	private boolean changedp()
	{
		boolean tc = textchanged;
		boolean bh = mh!=getBounds().height;
		boolean bv = mv!=getBounds().width;
		mh=getBounds().height;
		mv=getBounds().width;
		textchanged=false;
		if(bh||bv||oi==null)
		{
			oi = createImage(getBounds().width,getBounds().height);
			og = oi.getGraphics();
		}
		return (tc || bh || bv || oi==null);
	}
	
	public static boolean grc = true;
	public int mh;
	public int mv;
	
	private int drawT(String t, Font fo, Color c, int doneh)
	{
		og.setFont(fo);
		FontMetrics f = getFontMetrics(fo);
		LinkedList drawl=new LinkedList();
		int w = getBounds().width;
		int theH = getBounds().height;
		int h = f.getHeight();
		int hm = f.getMaxDescent();
		int n=0;
		char[] tdata=t.toCharArray();
		int tmp = 0;
		int currend=0;
		int currbegin=0;
		// int lnm = 1;
		// Font thefont = getFont();
		og.setColor(c);
		
		while(tmp < tdata.length)
		{
			// determine the position of the next word.
			while(
				(tmp < tdata.length)
				?
				tdata[tmp]!=' ' && tdata[tmp]!='\t' && tdata[tmp]!='\n'
				:
				false
				)
			{
				tmp++;
			}
			if (tmp!=tdata.length)tmp++;
			if( 
				( (tmp==tdata.length)
				  ? 
				  true 
				  : 
				  f.charsWidth(tdata,currbegin,tmp-currbegin)>w-2
					) 
				||
				(tdata[tmp-1] == '\n')
				)
			{
				if(currend==-1)//||tdata[tmp-1]=='\n')
				{
					currend=tmp;
				}
				if(tdata[tmp-1]=='\n'||tmp==tdata.length)
				{
					if( f.charsWidth(tdata,currbegin,tmp-currbegin)<w-2 )
					{
						currend=tmp;
						
						// og.drawChars(tdata,currbegin,(currend-currbegin),0,(h*n++)-hm);
						drawl.addElement(new String(tdata,currbegin,(currend-currbegin)));
						
						currbegin=currend;
						currend=-1;
					}
					else
					{
						//og.drawChars(tdata,currbegin,(currend-currbegin),0,(h*n++)-hm);
						drawl.addElement(new String(tdata,currbegin,currend-currbegin));
						currbegin=currend;
						currend=tmp;
						
						//og.drawChars(tdata,currbegin,(currend-currbegin),0,(h*n++)-hm);
						drawl.addElement(new String(tdata,currbegin,currend-currbegin));
						currbegin=currend;
						currend=-1;
					}
				}
				else
				{
					//og.drawChars(tdata,currbegin,(currend-currbegin),0,(h*n++)-hm);
					drawl.addElement(new String(tdata, currbegin, currend-currbegin));
					
					currbegin=currend;
					currend=-1;
				}
			}
			else
			{
				currend=tmp;
			}
			tmp++;
		}
		
		Enumeration theE = drawl.elements();
		while(theE.hasMoreElements())
		{
			String toPaint = theE.nextElement().toString();
			
			//System.out.println("drawing \""+toPaint+"\", 0, "+ (theH- (n*h)));
			
			og.drawString(toPaint,0,theH- ( (n++ * h) + doneh + hm + 1) );
		}
		
		return doneh+((drawl.size())*h);
	}
	
	public void update(Graphics g) {paint(g);}
	
	public void paint(Graphics g)
	{
		if (thel==null)
		{
			super.paint(g);
			return;
		}
		
		if(changedp())
		{
			og.setColor(getBackground());
			og.fillRect(0,0,getBounds().width,getBounds().height);
			//oi = createImage(getBounds().width,getBounds().height);
			//og = oi.getGraphics();
			//og.setColor(mColor);
			int i = 0;
			Font thef = BIG;
			Enumeration e = thel.elements();
			if(bg!=null && grc) tileImage(bg,og);
			
			while(e.hasMoreElements() && (i < getBounds().height) )
			{
				i = drawT(e.nextElement().toString(),thef,mColor,i);
				thef=LITTLE;
			}
		}
		g.drawImage(oi,1,1,this);
	}
	
	private Color mColor;
	
	public void setColor(Color m)
	{
		mColor=m;
	}
	
	private synchronized void imageSet(Image a)
	{
		bg=a;
		textchanged=true;
		repaint();
	}
	
	
	int image_width;
	int image_height;
	boolean done;
	
	String lastimage;
	
	public void setImage(String s)
	{
		//System.out.println("setting image, text");
		//System.out.println(s);
		//System.out.println(!s.equals(lastimage));
		//if(!s.equals( lastimage))
		//{
		//	lastimage=s;
		if(grc)imageSet(ImageServer.getImage(s,this));
		//}
	}
	
	int wdth;
	int hght;
	
	private Point getFLocation()
	{
		Point p = getLocationOnScreen();
		Container q=getParent();
		while( !( q instanceof Frame ))
		{
			q=q.getParent();
		}
		
		Point r = q.getLocationOnScreen();
		p.x-=r.x;
		p.y-=r.y;
		//System.out.print(p.x); System.out.print(','); System.out.println(p.y);
		return p;
	}
	
	final void tileImage(Image a, Graphics b)
	{
		wdth=a.getWidth(this);
		hght=a.getHeight(this);
		Point p = getFLocation();
		
		if(grc && ((wdth>0) && (hght>0)))
			for(int i = -(p.x%wdth);i<getBounds().width;i+=wdth)
			{
				for(int j = -(p.y%hght); j<getBounds().height;j+=hght)
				{
					b.drawImage(a,i,j,this); 
					//System.out.print(i);System.out.print(',');System.out.println(j);
				}
			}
	}
	/*
	  final void tileImage(Image a, Graphics b)
	  {
	  //System.out.println("image tiling...");
	  wdth=a.getWidth(this);
	  hght=a.getHeight(this);
	  if(grc && ((wdth>0) && (hght>0)))
	  for(int i = -1;i<getBounds().width;i+=wdth)
	  {
	  //System.out.println("Starting once...");
	  
	  for(int j = -1; j<getBounds().height;j+=hght)
	  {
	  //try {Thread.sleep(100);} catch (Exception e) {}
	  
	  b.drawImage(a,i,j,this);
	  }
	  //System.out.println("Going Once...");
	  }
	  }*/
	Image bg;
	
	
	Image oi;
	Graphics og;
	
	String tbuf;
}
