package twisted.reality.client.cx;
import twisted.reality.client.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.WindowListener;
import java.awt.event.WindowEvent;

import twisted.util.swing.TextThingy;
import twisted.util.swing.BackgroundThingy;
public class TextWindow extends CX implements WindowListener
{
	JFrame frame;
	TextThingy t;
	
	public void handleData(Object[] message)
	{
		String command = ((String)message[0]).intern();
		if(command == "t")
			frame.setTitle((String)message[1]);
		else if(command == "c")
			t.setText("");
		else if(command == "a")
			t.append((String)message[1]);
	}
	
	public void init()
	{
		frame = new JFrame("Untitled");
		BackgroundThingy b = new FaucetBGThingy();
		frame.getContentPane().setLayout(new BorderLayout());
		frame.getContentPane().add(b,BorderLayout.CENTER);
//		frame.setIconImage(Faucet.theIcon);
		frame.addWindowListener( this);
		frame.setResizable(true);
		frame.setSize(390,220);
		frame.setLocation(100,100);
		
		t=new TextThingy();
		t.setEditable(false);
		t.setFont(new Font("Helvetica",Font.BOLD,12));
		t.setText("");
		b.setLayout(new BorderLayout());
		b.add("Center",t);
		frame.setVisible(true);
	}
	
	public void destroy()
	{
		frame.dispose();
	}
	
	public void windowClosing(WindowEvent e) 
	{
		requestStopCX();
	}
	
	public void windowActivated(WindowEvent e) {}
	public void windowClosed(WindowEvent e) {}
	public void windowDeactivated(WindowEvent e) {}
	public void windowDeiconified(WindowEvent e) {}
	public void windowIconified(WindowEvent e) {}
	public void windowOpened(WindowEvent e) {}

}
