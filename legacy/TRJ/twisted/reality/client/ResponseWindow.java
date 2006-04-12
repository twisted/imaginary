package twisted.reality.client;
import java.awt.*;
import java.awt.image.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;
import java.net.*;
import javax.swing.*;
import javax.swing.*;
import twisted.util.awt.*;
import twisted.util.swing.*;
import twisted.util.*;

class ResponseWindow extends JFrame implements WindowListener
{

	public void windowOpened(WindowEvent e){}
	public void windowClosed(WindowEvent e){}
	public void windowIconified(WindowEvent e){}
	public void windowDeiconified(WindowEvent e){}
	public void windowDeactivated(WindowEvent e) {}
	public void windowActivated(WindowEvent e){}
	public void windowClosing(WindowEvent e)
	{
		// goAway();
		dispose();
	}
	
	public ResponseWindow(String str, String p, String def, Faucet mf, String thep)
	{
		super(p);
		BackgroundThingy b = new FaucetBGThingy();
		//	b.setImage(thep + "/dbg.tmx");
		this.setContentPane(b);
		setIconImage(SwingNozzle.theIcon);
		addWindowListener( this);setResizable(true);
		setSize(390,220);
		setLocation(100,100);
		t=new TextThingy(SwingNozzle.isMacOS);
		t.setEditable(true);
		t.setFont(SwingNozzle.font);
		t.setText(def);
		faucet=mf;
		key=str;
		b.setLayout(new BorderLayout());
		JPanel jp = new JPanel();
		jp.setOpaque(false);
		FlowLayout fl = new FlowLayout();
		fl.setHgap(2);
		fl.setVgap(1);
		jp.setLayout(fl);
		JButton jb;
		jp.add(jb=new JButton("OK"));
		jb.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent ae)
			{
				goAway();
			}
		});
		jp.add(jb=new JButton("Cancel"));
		jb.addActionListener(new ActionListener()
		{
			public void actionPerformed(ActionEvent ae)
			{
				dispose();
			}
		});
		
		b.add("Center",t);
		b.add("South",jp);
		setVisible(true);
	}
	
	private void goAway()
	{
		faucet.gotResponse(t.getText(),key);
		setVisible(false);
		dispose();
	}
	
	Faucet faucet;
	TextThingy t;
	String key;
}
