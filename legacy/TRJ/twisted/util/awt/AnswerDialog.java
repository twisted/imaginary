package twisted.util.awt;

import java.awt.*;
import java.awt.event.*;
import java.util.Hashtable;
import twisted.util.LinkedList;
import java.util.Enumeration;

public class AnswerDialog extends Dialog implements ActionListener, Runnable
{
	LinkedList theDlogs=new LinkedList();
	
	public AnswerDialog(String s, Frame f)
	{
		super(f,false);
		setLayout(new BorderLayout());
		add("Center",new Label(s));
		Panel p = new Panel();
		p.setLayout(new FlowLayout());
		Button b = new Button("OK");
		b.addActionListener(this);
		p.add(b);
		add("South",p);
		setResizable(false);
		Font font = p.getFont();
		if (font == null)
		{
			System.out.println("Java gave me a null font! D'oh!");
			setSize(300, 100);
		}
		else
		{
			FontMetrics thef = p.getFontMetrics(font);
			setSize(thef.stringWidth(s)+20,100);
		}
		Toolkit t = getToolkit();
		Dimension d = t.getScreenSize();
		Dimension sz = getSize();
		setLocation
			(
				(d.width/2)-(sz.width/2),
				(d.height/2)-(sz.height/2)
				);
		
		if(frames.get(f)!=null)
		{
			AnswerDialog ad = (AnswerDialog) frames.get(f);
			ad.addDlog(this);
		}
		else
		{
			theThread = new Thread(this);
			addDlog(this);
			frames.put(f,this);
			theThread.start();
		}
	}
	
	public void run()
	{
		Enumeration e = theDlogs.elements();
		while(e.hasMoreElements())
		{
			AnswerDialog o = (AnswerDialog)e.nextElement();
			o.doShow();
			o.dispose();
		}
		frames.remove(getParent());
	}
	
	Thread theThread;
	
	void addDlog(AnswerDialog ad)
	{
		theDlogs.addElement(ad);
		ad.theThread=theThread;
	}
	
	public void doShow()
	{
		setVisible(true);
		theThread.suspend();
	}
	
	public void stopShow()
	{
		theThread.resume();
	}
	
	static Hashtable frames=new Hashtable();
	
	public void actionPerformed(ActionEvent e)
	{
		stopShow();
	}
	
	public static void main(String[] args)
	{
		Frame a = new Frame("A");
		
		Frame b = new Frame("B");
		
		a.setSize(100,100);
		a.setLocation(300,300);
		
		a.setVisible(true);
		
		b.setSize(100,100);
		b.setLocation(100,100);
		
		b.setVisible(true);
		
		new AnswerDialog("Test One",a);
		new AnswerDialog("Test Two",a);
		new AnswerDialog("Test Three",a);
		
		
		new AnswerDialog("Test Zero", b);
		new AnswerDialog("Test Four",b);
		new AnswerDialog("Test Five",b);
		
	}
	
}
