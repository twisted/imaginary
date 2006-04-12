package twisted.reality.client;
import java.awt.*;
import java.awt.image.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;
import java.net.*;
import javax.swing.*;
import javax.swing.event.*;
import twisted.util.swing.*;
import twisted.util.*;
 
class LoginPanel extends JPanel implements Runnable
{
	public void updateUI()
	{
		super.updateUI();
		setOpaque(false);
	}
	
	public void gbl(Component c)
	{
		gridbag.setConstraints(c,constraints);
		add(c);
	}
	
	GridBagLayout gridbag;
	GridBagConstraints constraints;
	
	SwingNozzle msn;
	
	public LoginPanel(SwingNozzle sn)
	{
		JLabel lbl;
		msn=sn;
		gridbag = new GridBagLayout();
		setLayout(gridbag);
		constraints = new GridBagConstraints();
		setOpaque(false);
		
		constraints.fill=GridBagConstraints.BOTH;
		constraints.weightx=0.0;
		constraints.weighty=1.0;
		constraints.ipadx=3;
		gbl(lbl=new JLabel("Version:"));
		lbl.setFont(SwingNozzle.font);
		lbl.setHorizontalAlignment(SwingConstants.RIGHT);
		
		constraints.weightx=1.0;
		constraints.gridwidth = GridBagConstraints.REMAINDER;
		gbl(lbl=new JLabel("Java Faucet "+Faucet.version+", Protocol V"+Faucet.protoVer));
		lbl.setHorizontalAlignment(SwingConstants.CENTER);
		lbl.setFont(SwingNozzle.font);
		
		
		constraints.gridwidth = 1;
		constraints.weightx=0.0;
		gbl(lbl=new JLabel("User name:"));
		lbl.setHorizontalAlignment(SwingConstants.RIGHT);

		constraints.gridwidth = GridBagConstraints.REMAINDER;
		constraints.weightx=1.0;
		gbl(username = new JTextField("", 23));
		lbl.setFont(SwingNozzle.font);
		username.setFont(SwingNozzle.font);

		constraints.gridwidth = 1;
		constraints.weightx = 0.0;
		gbl(lbl=new JLabel("Password:"));
		lbl.setHorizontalAlignment(SwingConstants.RIGHT);
		lbl.setFont(SwingNozzle.font);

		constraints.gridwidth = GridBagConstraints.REMAINDER;
		constraints.weightx=1.0;
		gbl(password = new JPasswordField("",23));
		password.setEchoChar('*');
		
		constraints.gridwidth = 1;
		constraints.weightx = 0.0;
		gbl(lbl=new JLabel("Server:"));
		lbl.setHorizontalAlignment(SwingConstants.RIGHT);
		lbl.setFont(SwingNozzle.font);
		
		constraints.gridwidth=GridBagConstraints.REMAINDER;
		constraints.weightx=1.0;
		gbl(server = new JTextField("reality.divunal.com",30));
		
		password.setFont(SwingNozzle.font);
		
		server.setFont(SwingNozzle.font);
		constraints.weighty=0.0;
		JPanel p2 = new JPanel();
		p2.setOpaque(false);
		p2.setFont( SwingNozzle.font );
		JButton okbut=new JButton("Engage");
		p2.add(okbut);
		constraints.gridwidth=GridBagConstraints.REMAINDER;
		constraints.weightx=1.0;
		gbl(p2);
		okbut.addActionListener
			(new LoginAction());
		username.addActionListener(new UserAction());
		password.addActionListener(new LoginAction());
		
	}
	
	class UserAction implements ActionListener
	{
		public void actionPerformed(ActionEvent ae)
		{
			password.requestFocus();
			// username.setText("");
		}
	}
	
	final Runnable realThis=this;
	class LoginAction implements ActionListener
	{
		public void actionPerformed(ActionEvent ae)
		{
			SwingUtilities.invokeLater(realThis);
		}
	}
	
	JTextField server,username;
	JPasswordField password;
	Faucet faucet;
	
	public void run()
	{
		msn.loginWin.setCursor(new Cursor(Cursor.WAIT_CURSOR));
		try
		{
			String servport = server.getText();
			int colpos = servport.indexOf(':');
			String server;
			int port = 8889;
			if (colpos == -1)
				server = servport;
			else
			{
				server = servport.substring(0,colpos);
				port = Integer.parseInt(servport.substring(colpos+1));
			}
			final String oops = "Sorry, couldn't connect to "+server+" port " + port + ".\n";
			Faucet faucet;
			msn.gameWin=new GameWindow(faucet=new Faucet(msn, username.getText(), server,port,new String(password.getPassword())) );
			msn.gameWin.setVisible(true);
			faucet.start();
			msn.loginWin.setVisible(false);
			/*
			SwingUtilities.invokeLater(new Runnable()
			{
				public void run()
				{
					msn.gameWin.requestFocus();
					msn.gameWin.jtf.requestFocus();
					msn.gameWin.jtf.requestFocus();
					msn.gameWin.jtf.requestFocus();
					msn.gameWin.jtf.requestFocus();
				}
			});
			*/
		}
		catch (NumberFormatException e) 
		{
			new JAnswerDialog("Please use only numeric ports.", msn.loginWin);
		}
		catch (Exception e)
		{
			StringWriter sw = new StringWriter();
			PrintWriter pw = new PrintWriter(sw);
			e.printStackTrace(pw);
			pw.flush();
			sw.close();
			new JAnswerDialog("Error during login: "+sw.toString(),msn.loginWin);
		}
		msn.loginWin.setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
	}
}
