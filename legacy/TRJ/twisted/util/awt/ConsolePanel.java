package twisted.util.awt;

import java.awt.*;
import java.awt.event.*;


public class ConsolePanel extends Component
	implements KeyListener, FocusListener,MouseListener
{
	char currkey;
	int currx;
	int curry;
	StringBuffer theString;
	String thePrompt;
	char theCursor;
	private CPListener hearer;
	public boolean isFocusTraversable()
	{
		return true;
	}
	public void mouseClicked(MouseEvent e)
	{ requestFocus(); }
	public void mousePressed(MouseEvent e)
	{ requestFocus(); }
	public void mouseEntered(MouseEvent e)
	{}
	public void mouseExited(MouseEvent e)
	{}
	public void mouseReleased(MouseEvent e)
	{}
	public void focusGained(FocusEvent e){
		System.out.println("GOTFOCUS!");
	}
	public void focusLost(FocusEvent e){}
	public ConsolePanel(CPListener talkToThis)
	{
		super();
		//	addFocusListener(this);
		addKeyListener(this);
		addMouseListener(this);
		currx = 10;
		curry = 15;
		cursof=0;
		cmdhist= new CommandHistory("");
		cmdhist= new CommandHistory("",cmdhist);
		hearer = talkToThis;
		theCursor = '_';
		thePrompt = "> ";
		theString = new StringBuffer();
		setBackground(Color.black);
		setForeground(Color.white);
		talkToThis.setConsole(this);
	}
	
	public void setPrompt(String s)
	{
		thePrompt=s;
		repaint();
	}
	
	public Dimension getPreferredSize()
	{
		return new Dimension(100,20);
	}
	CommandHistory cmdhist;
	void prevcmd()
	{
		if(cmdhist.prev!=null)
		{
			cmdhist=cmdhist.prev;
			theString=new StringBuffer(cmdhist.command);
			cursof=theString.length();
			repaint();
		}
	}
	
	void nextcmd()
	{
		if(cmdhist.next!=null)
		{
			cmdhist=cmdhist.next;
			theString=new StringBuffer(cmdhist.command);
			cursof=theString.length();
			repaint();
		}
	}
	boolean charlock;
	public void keyPressed(KeyEvent e)
	{
		int keychar = e.getKeyChar();
		int key = e.getKeyCode();
		boolean handled =false;
		switch(key)
		{
		case KeyEvent.VK_UP:
			prevcmd();handled=true;
			break;
			
		case KeyEvent.VK_DOWN:
			nextcmd();handled=true;
			break;
			
		case KeyEvent.VK_LEFT:
			if(cursof>0) cursof--;handled=true;
			break;
			
		case KeyEvent.VK_RIGHT:
			if(cursof<theString.length()) cursof++;handled=true;
			break;
		case KeyEvent.VK_ESCAPE:
			theString.setLength(0); cursof=0; handled=true;
			break;
		}
		if(!handled && theString.length()==0)
		{
			handled=true;
			String theShortcut=null;
			switch (key)
			{
			case KeyEvent.VK_SEMICOLON:
				theShortcut="emote \" ";
			case KeyEvent.VK_QUOTE:
				if(theShortcut==null) theShortcut="say \"";

				theString=new StringBuffer(theShortcut);
				cursof=theString.length();
				handled = true;
				break;
			case KeyEvent.VK_NUMPAD0:
				if(theShortcut==null) theShortcut="go up";
			case KeyEvent.VK_NUMPAD1:
				if(theShortcut==null) theShortcut="go southwest";
			case KeyEvent.VK_NUMPAD2:
				if(theShortcut==null) theShortcut="go south";
			case KeyEvent.VK_NUMPAD3:
				if(theShortcut==null) theShortcut="go southeast";
			case KeyEvent.VK_NUMPAD4:
				if(theShortcut==null) theShortcut="go west";
			case KeyEvent.VK_NUMPAD5:
				if(theShortcut==null) theShortcut="go down";
			case KeyEvent.VK_NUMPAD6:
				if(theShortcut==null) theShortcut="go east";
			case KeyEvent.VK_NUMPAD7:
				if(theShortcut==null) theShortcut="go northwest";
			case KeyEvent.VK_NUMPAD8:
				if(theShortcut==null) theShortcut="go north";
			case KeyEvent.VK_NUMPAD9:
				if(theShortcut==null) theShortcut="go northeast";
				theString=new StringBuffer(theShortcut);
				keyDown(10,'\n');
				charlock=true;
				break;
				
			default:
				// do nothing
				handled=false;
			}
		}
		if(handled)
		{
			repaint();
		}
		charlock = handled;
	}
	
	public void keyTyped(KeyEvent e)
	{
		//char c = e.getKeyChar();
		if(charlock)
		{
			charlock=false;
			return;
		}
		char i = e.getKeyChar();
		keyDown((int)i,i);
		
	}
	
	public void keyReleased(KeyEvent e)
	{
	}
	
	public void keyDown(int key,char keychar)
	{
		int q = theString.length();
		switch(key)
		{
		case KeyEvent.VK_BACK_SPACE:
			if(cursof>0)
			{
				if(cursof==q)
				{
					theString.setLength(q-1);
				}
				else
				{
					String string = theString.toString();
					theString=new StringBuffer(string.substring(0,cursof-1)+(string.substring(cursof)));
				}
				cursof--;
			}
			break;
		case KeyEvent.VK_ENTER:
		case 141:
			//		case 10:
		case 13:
			if(theString.length() != 0)
			{
				if(isWaiting)
					freeString(theString.toString());
				else
					hearer.NowHearThis(theString.toString());
				while(cmdhist.next!=null) cmdhist=cmdhist.next;
				(cmdhist.prev=new CommandHistory(theString.toString(),cmdhist.prev)).next=cmdhist;
				theString.setLength(0);
				cursof=0;
			}
			break;	
		default:
			theString.insert(cursof++,keychar);
			break;
		}
		repaint();
	}
	
	public String getString(String tprmpt)
	{
		if(locked) return null;
		t = Thread.currentThread();
		
		
		locked = true;
		isWaiting = true;
		
		String tmpstr = thePrompt;
		thePrompt = tprmpt;
		
		repaint();
		
		t.suspend();
		
		
		String s2 = s;
		s=null;
		
		thePrompt = tmpstr;
		
		locked = false;
		isWaiting = false;
		
		return s2;
	}
	
	public void freeString(String theS)
	{
		s = theS;
		t.resume();
	}
	
	Thread t;
	String s;
	
	boolean locked;
	
	boolean isWaiting;
	
	public void update(Graphics g)
	{
		paint(g);
	}
	
	FontMetrics f;
	
	int mh;
	int mv;
	
	public void paint( Graphics g )
	{
		if(f==null)f=getFontMetrics(getFont());
		g.setFont(getFont());
		//System.out.println("<1>");
		boolean bh = mh != getBounds().height;
		boolean bv = mv != getBounds().width;
		boolean on = oi == null;
		mh=getBounds().height;
		mv=getBounds().width;
		if(bh||bv||on)
		{
			oi = createImage(mv,mh);
			og = oi.getGraphics();
			//System.out.println("<2> "+mv+' '+mh);
		}
		
		//System.out.println("<3>");
		
		og.setColor(Color.black);
		og.fillRect(0,0,mv,mh);
		og.setColor(Color.white);
		og.setFont(getFont());
		//System.out.println("<4>");
		String s = theString.toString();
		String t = thePrompt+s;
		int x = 0;
		//System.out.println("<5>");
		//System.out.println(f.stringWidth(t));
		//System.out.println("<6>");
		//System.out.println(f.stringWidth(thePrompt+(s.substring(0,cursof-x))));
		while( (f.stringWidth(t) > (mv-currx)))
		{
			x++;
			//System.out.println(t);
			t=thePrompt+"..."+s.substring(x,cursof);
			//System.out.println( f.stringWidth(t));
			
			//System.out.println(x);
		}
		
		//System.out.println("<7>");
		//System.out.println(f.stringWidth(t) > 640);
		og.drawString(t,currx,curry);
		//System.out.println("<8>"+currx+" "+curry);
		og.drawString(
			""+theCursor,
			currx+((x>0)?f.stringWidth(t):f.stringWidth(t.substring(0,cursof+thePrompt.length()))),
			curry);
		//System.out.println(cursof);
		//System.out.println("<5>");
		g.drawImage(oi,0,0,this);
	}
	int cursof;
	Image oi;
	Graphics og;
}
