package twisted.util.awt;

import java.awt.*;
import java.awt.image.*;
import java.awt.event.*;

class ImageWind extends Frame implements Runnable
{
	String[] images;
	Imageview image;
	ImageWind(Imageview i, String[] s)
	{
		images=s;
		image=i;
		setLayout(new BorderLayout());
		addWindowListener( new WindowListener() {
			
			public void windowClosed(WindowEvent event) {}
			
			public void windowDeiconified(WindowEvent event) {
			}
			
			public void windowIconified(WindowEvent event) {
			}
			
			public void windowActivated(WindowEvent event) {
			}
			
			public void windowDeactivated(WindowEvent event) {
			}
			
			public void windowOpened(WindowEvent event) {
			}
			
			public void windowClosing(WindowEvent event) {
				System.exit(0);
			}
		}
			);
		setSize(100,100);
		show();
		Thread t = new Thread(this);
		t.start();
	}
	
	public void run()
	{
		int i = 0;
		while(true)
		{
			setVisible(false);
			image.setImage(images[i]);
			setVisible(true);
			setSize(image.preferredSize());
			image.repaint();
			try { Thread.sleep(5000); }
			catch(Exception e) {}
			if(i>=images.length-1) i=0; else i++;
		}
	}
}

public class Imageview extends Canvas
{
	public void paint(Graphics g)
	{
		if(image == null) 
		{
			super.paint(g);
		}
		else
		{
			if(done && grc)
			{
				g.drawImage(image,1,1,
							// uncomment this line for images which are scaled to the height and width
							// of the drawing area
							// ---
							
							//bounds().width,bounds().height,
							this);
				//System.out.println("Drawing image...");
			}
			else 
			{
				super.paint(g);
				g.drawString("Loading...",bounds().height/2,bounds().width/2);
			}
		}
	}
	/*
	  public void repaint()
	  {
	  paint(getGraphics());
	  }
	*/
	public void update(Graphics g)
	{
		paint(g);
	}
	
	int image_width;
	int image_height;
	
	public Dimension preferredSize()
	{
		return new Dimension(image_width,image_height);
	}
	
	boolean done;
	public boolean imageUpdate(Image img, int infoflags, int x, int y, int width, int height)
	{
		if ((infoflags & ImageObserver.ALLBITS) != 0)
		{
			image_width = image.getWidth(null);
			image_height = image.getHeight(null);
			done = true;
			repaint();
			if(blocker != null)
			{
				blocker.resume();
				blocker=null;
			}
			return false;
		}
		return true;
	}
	/*
	  private void setImage(Image a)
	  {
	  if(image != null)
	  {
	  image.flush();
	  }
	  image=a;
	  if(a!=null)
	  done = Toolkit.getDefaultToolkit().prepareImage(a,a.getWidth(this),a.getHeight(this),this);
	  done = false;
	  repaint();
	  }
	*/
	private void setImage(Image a)
	{
		//System.out.println("SETTING IMAGE");
		Image qi=image;
		image=a;
		if(a!=null) startwait(a);
		if(qi != null)
		{qi.flush();}
		repaint();
		//System.out.println("DONE.");
	}
	
	String lastimage;
	public void setImage(String s)
	{
		if(!s.equals(lastimage))
		{
			lastimage=s;
			if(grc) setImage(Toolkit.getDefaultToolkit().getImage(s));
		}
		try{Thread.sleep(10);}catch(Exception e){}
	}
	
	public void startwait(Image a)
	{
		Toolkit.getDefaultToolkit().prepareImage(a,a.getWidth(this),a.getHeight(this),this);
		blocker=Thread.currentThread();
		blocker.suspend();
	}
	
	public void waitUntilDone()
	{
		/*if(!done)
		  {
		  blocker = Thread.currentThread();
		  blocker.suspend();
		  }*/try
		  {
			  Thread.sleep(400);
		  }catch(Exception e) {}
	}
	
	public static void main(String args[])
	{
		grc=true;
		Imageview a = new Imageview();
		//System.out.println("Image:" + args[0]);
		new ImageWind(a,args);
	}
	
	private Thread blocker;
	private Image image;
	public static boolean grc=true;
}
