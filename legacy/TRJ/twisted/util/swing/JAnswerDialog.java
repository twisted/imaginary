package twisted.util.swing;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.Hashtable;
import twisted.util.LinkedList;
import java.util.Enumeration;

public class JAnswerDialog extends JDialog implements ActionListener, Runnable
{
	LinkedList theDlogs=new LinkedList();
	
	public JAnswerDialog(String s, Frame f)
	{
		super(f,false);
		setTitle("Error");
		JTextArea text = new SpecialJTextArea(s,8,38);
		text.setEditable(false);
		text.setMargin(new Insets(10,10,10,10));
		text.setWrapStyleWord(true);
		text.setLineWrap(true);
		setFont(Font.decode("Dialog"));
		getContentPane().setLayout(new BorderLayout());
		getContentPane().add("Center",new JScrollPane(text));
		JPanel p = new JPanel();
		p.setLayout(new FlowLayout());
		JButton b = new JButton("OK");
		b.addActionListener(this);
		p.add(b);
		getContentPane().add("South",p);
		setResizable(false);
		Dimension ps = text.getPreferredSize();
		setSize(ps.width, ps.height+40);
		// pack();
		Dimension d = getToolkit().getScreenSize();
		Dimension sz = getSize();
		setLocation
			(
				(d.width/2)-(sz.width/2),
				(d.height/2)-(sz.height/2)
				);
		
		if(frames.get(f)!=null)
		{
			JAnswerDialog ad = (JAnswerDialog) frames.get(f);
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
			JAnswerDialog o = (JAnswerDialog)e.nextElement();
			o.doShow();
			o.dispose();
		}
		frames.remove(getParent());
	}
	
	Thread theThread;
	
	void addDlog(JAnswerDialog ad)
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
		JFrame a = new JFrame("A");
		
		JFrame b = new JFrame("B");
		
		a.setSize(100,100);
		a.setLocation(300,300);
		
		a.setVisible(true);
		
		b.setSize(100,100);
		b.setLocation(100,100);
		
		b.setVisible(true);
		
		new JAnswerDialog("Test One",a);
		new JAnswerDialog("Test Two",a);
		new JAnswerDialog("Test Three",a);
		
		
		new JAnswerDialog("Test Zero", b);
		new JAnswerDialog("Test Four",b);
		new JAnswerDialog("Test Five",b);
		
	}
	
}
