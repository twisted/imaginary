package twisted.util.awt;
//import java.awt.Component;
import twisted.util.CharArray;
import java.awt.*;
import java.awt.event.*;
import java.util.Enumeration;
import java.util.StringTokenizer;
import java.util.Vector;

class TexterWord
{
	TexterWord()
	{
		dirty=true;
	}
	int wordlen;
	char[] text;
	boolean dirty;
	public void retext(char[] n, int nwl)
	{
		//newwordlen
		if(drawn) eraseme();
		int nwidth;
		Texter thet = sLine.theTexter;
		if(wordlen==0)
		{
			wordlen=n.length;
			text=n;
		}
		else
		{
			wordlen=nwl;
			text=n;
		}
		FontMetrics fnt = thet.thefonter;
		if(n.length==1)
		{
			switch(n[0])
			{
			case '\n':
				isNewline=true;
			case ' ':
			case '\t':
				isSpace=true;
			}
		}
		
		
		nwidth=fnt.charsWidth(text,0,wordlen);
		
		if(nwidth!=mwidth)
		{
			System.out.println("WIDTH now "+nwidth);
			mwidth=nwidth;
			dirty=true;
		}else
		{
			System.out.println("WIDTH not SET!");
		}
	}
	
	public final TexterWord newWord(char a)
	{
		TexterWord newword = new TexterWord();
		char[] n = new char[1];
		n[0]=a;
		newword.setLine(sLine);
		newword.retext(n,1);
		return newword;
	}
	
	final void linkafter(TexterWord after)
	{
		after.prevWord=this;
		after.nextWord=nextWord;
		if(nextWord != null) nextWord.prevWord=after;
		nextWord=after;
		after.setLine(sLine);
	}
	
	final void linkbefore(TexterWord before)
	{
		before.prevWord=prevWord;
		before.nextWord=this;
		prevWord.nextWord=before;
		prevWord=before;
		if(before.prevWord!=null) before.setLine(prevWord.sLine);
		else before.setLine(sLine);
	}
	
	public synchronized void keyHit(char c)
	{
		
	}
	
	int indexFromPixels(int pixels)
	{
		int i;
		int pix=pixels;
		for(i=0;i<wordlen;i++)
		{
			pix-=sLine.theTexter.thefonter.charWidth(text[i]);
			if(pix<=0) break;
		}
		return i;
	}
	
	int pixelsFromIndex(int index)
	{
		if(index > wordlen) return pixelsFromIndex(wordlen);
		
		return sLine.theTexter.thefonter.charsWidth(text,0,index);
	}
	
	public void insertAt(int i)
	{
		//eraseme();
		insertionPoint=i;
		System.out.println("changing insertion");
		drawme();
	}
	
	int insertionPoint=-1;
	
	boolean isNewline;
	boolean isSpace;
	
	public synchronized int width()
	{
		return mwidth;
	}
	
	public synchronized int pos()
	{
		if(mpos==0 && isSpace) System.out.println("This bug CONFIRMED.");
		return mpos;
	}
	
	private int mwidth;
	private int mpos;
	
	void repos()
	{
		int npos=sLine.whereIs(this);
		if(npos!=mpos)
		{
			System.out.println("POS is now:"+npos);
			if(drawn) eraseme();
			if(isSpace && npos == 0) System.out.println("CONFIRMED this bug...");
			if(isSpace && npos != 0) System.out.println("BEARS FURTHER INVESTIGATION");
			mpos=npos;
			dirty=true;
		}
		else
		{
			System.out.println("POS not changed");
		}
	}	
	
	synchronized boolean layout(Graphics g, int height, int ascent, int descent)
	{
		
		boolean ret = false;
		repos();
		if(isSpace)
		{
			if(nextWord != null)
			{
				if(isNewline)
				{
					if (nextWord.sLine != sLine.nextLine())
					{
						linebreak();
						ret= true;
					}
				}
				else
				{
					if(nextWord.sLine == null) nextWord.setLine(sLine);
					if((sLine.whereIs(nextWord) + nextWord.width()) > sLine.maxWidth())
						// if it should be on the next line
					{
						if (nextWord.sLine.myFirstWord != nextWord)
							// and it isn't
						{
							// stick it on the next line and tell it to re-layout itself.
							linebreak();
							ret= true;
						}
						else
							// and it is
						{
							// you're done -- even though you position is different
							// (so later calls to dirty will succeed)
							ret= false;
						}
					}
					else
						// if it shouldn't be on the next line
					{
						if(nextWord.sLine!=sLine)
							// and it is
						{
							// stick it back on the right line and tell it to fix itself!
							nextWord.setLine(sLine);
							ret=true;
						}
					}
				}
			}
		}
		else
		{
			if(nextWord!=null)
			{
				if(nextWord.sLine != sLine) 
				{
					nextWord.setLine(sLine);
					ret=true;
				}
			}
		}
		
		if(dirty)
		{
			dirty=false;
			ret=true;
		}
		return ret;
	}
	
	void eraseme()
	{
		int height
			= sLine.theTexter.maxheight;
		int ascent
			= sLine.theTexter.maxascent;
		int descent
			= sLine.theTexter.maxdescent;
		Graphics g
			= sLine.theTexter.og;
		
		drawn=false;
		if(g == null) return;
		int l = pos();
		int r = width();
		if( (nextWord != null) ? nextWord.sLine.myFirstWord==nextWord:true)
		{
			// what I want to know is: how the fuck does this change the value of L????
			System.out.println("L EQUALS" + l);
			r=sLine.theTexter.getBounds().width-(pos()+width()+2);
		}
		
		int tp = (sLine.lineno)*height;
		
		int t = tp-ascent;
		int b = tp+descent;
		
		g.clearRect(l,b,r,b-t); 
		System.out.println("Erasing rect:"+l+","+b+","+r+","+(b-t));
		//g.drawRect(l,b,r,b-t);
	}
	
	public void reformat()
	{
		dirty=true;
		eraseme();
		format();
	}
	
	boolean drawn=false;
	
	public synchronized void format()
	{
		int height
			= sLine.theTexter.maxheight;
		int ascent
			= sLine.theTexter.maxascent;
		int descent
			= sLine.theTexter.maxdescent;
		Graphics g
			= sLine.theTexter.og;
		TexterWord t = this;
		if(g == null) return;
		while(t != null)
		{
			if(!t.layout(g,height,ascent,descent)) break;
			t=t.nextWord;
		}
		
		t=this;
		while(t != null)
		{
			if (t.drawn) return;
			t.drawme();
			t=t.nextWord;
		}
	}
	
	private final void linebreak()
	{
		sLine.nextLine().myFirstWord=nextWord;
		nextWord.setLine(sLine.nextLine());
	}
	//self-explanitory
	// TexterWord is a list that's maintained that contains EVERY word
	// the links continue around the end of lines.
	TexterWord nextWord;
	TexterWord prevWord;
	//duh
	// the line i'm in
	TexterLine sLine;
	
	public void setLine(TexterLine t)
	{
		if(t != sLine)
		{
			if(drawn) eraseme();
			dirty=true;
			sLine=t;
		}
	}
	
	/*
	  A word about selections:
	  -2 is 'not selected'
	  -1 is 'off the left' or 'off the right'
	*/
	
	int beginSelect= -2;
	int endSelect= -2;
	
	synchronized void drawme()
	{
		int height
			= sLine.theTexter.maxheight;
		int ascent
			= sLine.theTexter.maxascent;
		int descent
			= sLine.theTexter.maxdescent;
		Graphics g
			= sLine.theTexter.og;
		if (g==null) return;
		if(!isSpace) g.drawChars(text,0,wordlen,pos(),(1+sLine.lineno)*height);
		if(insertionPoint != -1)
		{
			int l=pos()+pixelsFromIndex(insertionPoint);
			int tp = (1+sLine.lineno)*height;
			int t = tp-ascent;
			int b = tp+descent;
			g.drawLine(l,t,l,b-1);
		}
		int selleft;
		int selright;
		if(beginSelect != -2)
		{
			if(beginSelect == -1) { selleft=0; } else { selleft = beginSelect; }
			if(endSelect == -1) { selright=wordlen; } else { selright = endSelect; }
			Color thebg = sLine.theTexter.getBackground();
			g.setXORMode(thebg);
			int l = pos()+pixelsFromIndex(selleft);
			int r = pos()+pixelsFromIndex(selright);
			int tp = (1+sLine.lineno)*height;
			int t = tp-ascent;
			int b = tp+descent;
			// int b = sLine.lineno*height;
			g.fillRect(l,b,r-l,t-b);
			g.setPaintMode();
		}
		drawn=true;
	}
}

class START extends TexterWord
{
	public START()
	{super();}
	public synchronized void keyHit(char c)
	{
		if (c == (char) 8) return;
		if(nextWord == null)
		{
			TexterWord t=newWord(c);
			linkafter(t);
			sLine.theTexter.setInsertion(nextWord,1);
			drawn=false;
			nextWord.dirty=true;
			reformat();
			//return;
		}
		else
		{
			sLine.theTexter.setInsertion(nextWord,0);
			nextWord.keyHit(c);
		}
	}
	
	public synchronized void nreformat()
	{
		int height
			= sLine.theTexter.maxascent;
		int ascent
			= sLine.theTexter.maxdescent;
		int descent
			= sLine.theTexter.maxdescent;
		Graphics g
			= sLine.theTexter.og;
		TexterWord t = this;
		if(g == null) return;
		while(t != null)
		{
			t.dirty=true;
			if(!t.layout(g,height,ascent,descent)) break;
			t=t.nextWord;
		}
		
		t=this;
		while(t != null)
		{
			t.drawn=false;
			t.drawme();
			t=t.nextWord;
		}
	}
	
	public void retext(char[] n)
	{ return; }
	public int pos()
	{ return 0; }
	public int width()
	{ return 0; }
	public int indexFromPixels(int k)
	{ return 0; }
	public int pixelsFromIndex(int k)
	{ return 0; }
}

/**
   How does a TexterLine get Textered?
   the line contains a vector of words
   the words can be added and removed at a moment's notice tho!
   how do you manage the words
   the words move by themselves because they know where they are
   texterlines set the IsNewLine bit in words
   
*/

class TexterLine
{
	public TexterLine (Texter t)
	{
		t.lines.insertElementAt(this,t.currlineno++);
		theTexter=t;
	}
	// buffer calculations are the calculations regarding the
	// buffer of characters to draw and therefore this function
	// does NOT contain leading whitespaces and the like.
	// except in the case of tabs.
	
	// this is just to get the data out.
	
	// NOTE: we should really be calling PeekEvents and seeing
	// if the next event is a keyhit.  DO NOT CALL THIS MULTIPLE
	// TIMES WHEN DOING THAT.  This can be slow.
	// this is actually WRONG, but ok
	public int lineno=0;
	char[] calculateBuffer()
	{
		TexterWord word = myFirstWord;
		char[] tmp=null;
		while((word!=null)?word.sLine == this:false)
		{
			tmp=CharArray.cat(tmp,word.text);
			word=word.nextWord;
		}
		return tmp;
	}
	
	int whereIs(TexterWord inWord)
	{
		TexterWord word = myFirstWord;
		int i=0;
		System.out.println("If no THIS WORD then THIS DEAD");
		
		while(/*word.sLine == this &&*/ word!=inWord)
		{
			System.out.println("This word: "+word.width());
			i+=word.width();
			word=word.nextWord;
		}
		System.out.println("Total: "+i);
		return i;
	}
	
	int width()
	{
		TexterWord word = myFirstWord;
		
		int i=0;
		while(word.sLine == this)
		{
			i+=word.width();
		}
		return i;
	}
	
	Texter theTexter;
	
	public final TexterLine nextLine()
	{
		if(theNextLine==null)
		{
			theNextLine=new TexterLine(theTexter);
			// we're never disposing of these for now, rationale
			// being that there always might be reflowing
			// text coming around - I wouldn't class it as a 
			// memory leak, 'cause it only uses the mem if you
			// have that many lines in the first place.
			theNextLine.lineno=lineno+1;
			theNextLine.thePreviousLine=this;
		}
		return theNextLine;
	}
	
	public TexterWord wordAt(int xcoord)
	{
		TexterWord word=myFirstWord;
		int i = 0;
		while(word.sLine == this)
		{
			i+=word.width();
			if((i >= xcoord)||word.nextWord==null) return word;
			word=word.nextWord;
		}
		return null; // this means WHUPS! I clicked outside of the bounds of this component!
	}
	
	public int maxWidth()
	{
		return theTexter.maxWidth();
	}
	
	TexterLine theNextLine;
	TexterLine thePreviousLine;
	// gotta monitor this changing
	TexterWord myFirstWord;
}

/**
   Texter
   A simple TextField replacement.
   
   (SIMPLE he says! This is a SIMPLE replacement!!!)
*/

public class Texter extends Canvas implements MouseListener, KeyListener, FocusListener
{
	public void keyPressed(KeyEvent k)
	{}
	public void keyReleased(KeyEvent k)
	{}
	public void keyTyped(KeyEvent k)
	{
		theInserter.keyHit(k.getKeyChar());
		repaint();
	}
	public void mouseClicked(MouseEvent e)
	{
		int x = e.getX();
		int y = e.getY();
		
		int height = thefonter.getHeight();
		TexterWord word = lineAt(y/height).wordAt(x);
		if(word != null)
		{
			setInsertion(word, word.indexFromPixels( x-word.pos() ));
			// theInserter.keyHit('a');
		}
		repaint();
	}
	
	TexterWord theInserter;
	
	synchronized void setInsertion(TexterWord w, int i)
	{
		if(theInserter != null)
		{
			theInserter.insertAt(-1);
		}
		theInserter=w;
		if(w!=null)
			w.insertAt(i);
	}
	
	public TexterLine lineAt(int i)
	{
		return (TexterLine) lines.elementAt(i);
	}
	
	public void mouseEntered(MouseEvent e) {}
	
	public void mouseExited(MouseEvent e) {}
	
	public void mousePressed(MouseEvent e) {}
	
	public void mouseReleased(MouseEvent e) {}
	
	public void focusGained(FocusEvent f)
	{
		//System.out.println("I've got the focus now.");
	}
	
	public void focusLost(FocusEvent f)
	{
		
		//System.out.println("I've lost the focus now.");
	}
	
	int currlineno=0;
	
	void init()
	{
		myLine = new TexterLine(this);
		firstWord=new START();
		firstWord.setLine(myLine);
		myLine.myFirstWord=firstWord;
		setInsertion(firstWord,0);
	}
	
	public Texter()
	{
		currlineno=0;
		lines=new Vector();
		setFont(new Font("TimesRoman",Font.PLAIN,12));
		thefonter=getFontMetrics(getFont());
		
		maxheight=thefonter.getHeight();
		maxascent=thefonter.getMaxAscent();
		maxdescent=thefonter.getMaxDescent();
		
		addMouseListener(this);
		addKeyListener(this);
		addFocusListener(this);
		requestFocus();
		
		init();
	}
	
	public boolean isFocusTraversable()
	{
		return true;
	}
	
	FontMetrics thefonter;
	TexterWord myWord;
	START firstWord;
	TexterLine myLine;
	Vector lines;
	int lastlineno;
	
	public void setText(String str)
	{
		init();
		StringTokenizer toq = new StringTokenizer(str," \t\n",true);
		myWord=firstWord;
		while(toq.hasMoreElements())
		{
			TexterWord myprev = myWord;
			myWord=new TexterWord();
			myprev.nextWord=myWord;
			String tok=toq.nextToken();
			char[] c = new char[tok.length()];
			tok.getChars(0,tok.length(),c,0);
			myWord.setLine(myLine);
			myWord.retext(c,c.length);
			myWord.prevWord=myprev;
			
		}
		firstWord.reformat();
	}
	
	public String getText()
	{
		TexterWord t = firstWord;
		StringBuffer s = new StringBuffer();
		while (t!=null)
		{
			if(t.text != null) s.append(t.text);
			t=t.nextWord;
		}
		return s.toString();
	}
	
	public int maxWidth()
	{
		return getBounds().width;
	}
	
	public void update(Graphics g)
	{
		paint(g);
	}
	
	public void paint(Graphics g)
	{
		if(getBounds().height != oldh || getBounds().width != oldw)
		{
			oldh = getBounds().height;
			oldw = getBounds().width;
			
			oi=createImage(getBounds().width,getBounds().height);
			og=oi.getGraphics();
			og.setFont(getFont());
			firstWord.nreformat();
		}
		g.drawImage(oi,0,0,null);
	}
	
	Image oi;
	Graphics og;
	
	int oldw;
	int oldh;
	
	int maxdescent;
	int maxascent;
	int maxheight;
	
	public static void main(String args[])
	{
		Frame f = new Frame();
		f.setSize(300,200);
		
		Texter e = new Texter(); //
		f.add(e);
		//e.setText("You'll learn to love the price you pay - trust me, dear, you're better off this way!  Put together sun and sister moon.  I'll be hiding in your dirty room.");
		f.setVisible(true);
		e.requestFocus();
	}
}
