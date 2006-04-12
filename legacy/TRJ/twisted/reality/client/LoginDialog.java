package twisted.reality.client;

import java.awt.*;
import java.awt.image.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;
import java.net.*;
import javax.swing.*;
import javax.swing.event.*;
import twisted.util.awt.*;
import twisted.util.swing.*;
import twisted.util.*;

class LoginDialog extends JFrame implements WindowListener
{
	public LoginDialog(SwingNozzle sn)
	{
		super("Reality Faucet Login");
		setIconImage(SwingNozzle.theIcon);
		addWindowListener(this);
		setSize(300,160);
		setResizable(false);
		theBack = new FaucetBGThingy();
		this.setContentPane(theBack);
		theBack.setLayout(new BorderLayout());
		theBack.add("Center",mylp=new LoginPanel(sn));
		Dimension d = Toolkit.getDefaultToolkit().getScreenSize();
		setLocation((d.width/2)-(getBounds().width/2),(d.height/2)-(getBounds().height/2));
	}
	LoginPanel mylp;
	public BackgroundThingy theBack;
	
	public void windowOpened(WindowEvent e)
	{
	}
	public void windowClosed(WindowEvent e)
	{
	}
	public void windowIconified(WindowEvent e)
	{
	}
	public void windowDeiconified(WindowEvent e)
	{
	}
	public void windowActivated(WindowEvent e)
	{
		mylp.username.requestFocus();
	}
	public void windowDeactivated(WindowEvent e)
	{
	}
	public void windowClosing(WindowEvent e)
	{
		/* Should this call SwingNozzle.handleQuit instead? Probably...	*/
		if(SwingNozzle.isMacOS)
		{
			Window window = new Window(this);
			window.setBounds(-500, -500, -400, -400);
			window.show();
		}
		System.exit(0);
	}
}
