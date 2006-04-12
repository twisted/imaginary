package twisted.reality.client;

import javax.swing.*;
import javax.swing.text.*;
import javax.swing.event.*;
import java.awt.*;
import java.awt.image.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;
import java.net.*;
import twisted.util.swing.*;
import twisted.util.awt.*;
import twisted.util.*;
import javax.swing.tree.*;

class GameWindow extends JFrame implements WindowListener
{
	public void windowActivated(WindowEvent e)
	{
		jtf.requestFocus();
	}
	public void windowDeactivated(WindowEvent e){}
	public void windowOpened(WindowEvent e){}
	public void windowOpening(WindowEvent e){}
	public void windowClosed(WindowEvent e){}
	public void windowClosing(WindowEvent e)
	{
		faucet.bye();
	}
	public void windowIconified(WindowEvent e){}
	public void windowDeiconified(WindowEvent e){}
	
	public void requestResponse(String num, String prmpt, String defvl)
	{
		new ResponseWindow(num,prmpt,defvl,faucet,SwingNozzle.currentTheme);
	}
	
	public GameWindow(Faucet f)
	{
		super("Reality Faucet");
		setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
		setIconImage(SwingNozzle.theIcon);
		addWindowListener(this);
		setSize(600,460);
		faucet=f;
		Dimension d = Toolkit.getDefaultToolkit().getScreenSize();
		
		setLocation((d.width/2)-(600/2),(d.height/2)-(460/2));
		
		theBack=new FaucetBGThingy();
		theBack.setLayout(new BorderLayout());
		
		setContentPane(theBack);
		
		jtf = new HistoryTextField ();
		
		{
			Keymap map = jtf.getKeymap();
			
			assoc(KeyEvent.VK_NUMPAD0,"go up",map);
			assoc(KeyEvent.VK_NUMPAD8,"go north",map);
			assoc(KeyEvent.VK_NUMPAD9,"go northeast",map);
			assoc(KeyEvent.VK_NUMPAD7,"go northwest",map);
			assoc(KeyEvent.VK_NUMPAD4,"go west",map);
			assoc(KeyEvent.VK_NUMPAD1,"go southwest",map);
			assoc(KeyEvent.VK_NUMPAD2,"go south",map);
			assoc(KeyEvent.VK_NUMPAD3,"go southeast",map);
			assoc(KeyEvent.VK_NUMPAD6,"go east",map);
			assoc(KeyEvent.VK_NUMPAD5,"go down",map);
			tassoc(KeyEvent.VK_QUOTE,"say \"",map);
			tassoc(KeyEvent.VK_SEMICOLON,"emote \"",map);
		}
		
		jtf.setFont(SwingNozzle.font);
		jtf.addActionListener(new TRMutableListener());
		jtf.addKeyListener(new JTFCommandKeyListener());
		// jtf.setOpaque(false);

		theName = new TextThingy (jtf);
		FontMetrics tnfm = getFontMetrics(SwingNozzle.font);
		theName.setPreferredSize(new Dimension(600,tnfm.getHeight()+tnfm.getMaxDescent()));
		theName.setFont(SwingNozzle.font);
		
		theDescription = new TextThingy(jtf);
		theDescription.setPreferredSize(new Dimension(420,230));
		theDescription.setMinimumSize(new Dimension(0,0));
		theDescription.setFont(SwingNozzle.font);
		
/*		theStuff = new TextThingy(jtf);
		theStuff.setPreferredSize(new Dimension(180,230));
		theStuff.setMinimumSize(new Dimension(0,0));
		theStuff.setFont(SwingNozzle.font);*/
		
		theStuff = new WrappableJTree();
		theStuff.setFont(SwingNozzle.font);
		theStuff.setOpaque(false);
		theStuff.setCellRenderer(new TextAreaTreeCellRenderer());
		
		JScrollPane stuffScroll = new JScrollPane(theStuff);
		stuffScroll.setOpaque(false);
		stuffScroll.setPreferredSize(new Dimension(180,230));
		stuffScroll.setMinimumSize(new Dimension(0,0));
		
		
		topPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT,
								 theDescription,
								 stuffScroll);
		topPane.setPreferredSize(new Dimension(600,230));
		topPane.setMinimumSize(new Dimension(0,0));
		topPane.setContinuousLayout(true);
		topPane.setOpaque(false);
		
		theHappenings = new TextThingy(jtf);
		theHappenings.setPreferredSize(new Dimension(600,230));
		
		theHappenings.setMinimumSize(new Dimension(600,100));
		theHappenings.setFont(SwingNozzle.font);
		
		mainPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
								  topPane,
								  theHappenings);
		mainPane.setContinuousLayout(true);
				
		mainPane.setOpaque(false);

		theBack.add(theName,BorderLayout.NORTH);
		theBack.add(mainPane,BorderLayout.CENTER);
		theBack.add(jtf,BorderLayout.SOUTH);
	}
	
	void assoc(int key, String s, Keymap map)
	{
		KeyStroke ks = KeyStroke.getKeyStroke(key,0);
		map.removeKeyStrokeBinding(ks);
		map.addActionForKeyStroke(ks, new TRAction(s));
	}
	void tassoc(int key, String s, Keymap map)
	{
		KeyStroke ks = KeyStroke.getKeyStroke(key,0);
		map.removeKeyStrokeBinding(ks);
		map.addActionForKeyStroke(ks, new TextSetAction(s));
	}
	
	class TextSetAction extends AbstractAction implements Runnable
	{
		String command;
		public TextSetAction(String toRun)
		{
			command=toRun;
		}
		
		public void actionPerformed(ActionEvent ae)
		{
			SwingUtilities.invokeLater(this);
		}
		
		public void run()
		{
			if (!command.equals("") && jtf.getText().length() < 2)
			{
				jtf.setText(command+"\"");
				jtf.setCaretPosition(command.length());
			}
		}
	}

	class TRAction extends AbstractAction implements Runnable
	{
		String command;
		public TRAction(String toRun)
		{
			command=toRun;
		}
		
		public void actionPerformed(ActionEvent ae)
		{
			SwingUtilities.invokeLater(this);
		}
		
		public void run()
		{
			if (!command.equals("") && jtf.isEnabled())
			{
				jtf.setText(command);
				jtf.setEnabled(false);
				faucet.parseInput(command);
			}
		}
	}
	
	class TRMutableListener implements ActionListener
	{
		/** let's just assume it's jtf **/
		public void actionPerformed(ActionEvent ae)
		{
			new TRAction(jtf.getText()).actionPerformed(ae);
		}
	}
	
	/* Yuck hack. See comment in SwingNozzle about KeyMaps not working right */
	class JTFCommandKeyListener implements KeyListener
	{
		public void keyTyped(KeyEvent e)
		{
			char kc = e.getKeyChar();
			int mod = e.getModifiers();
			if((mod & KeyEvent.CTRL_MASK) != 0 || (mod & KeyEvent.META_MASK) != 0)
			{
				if(kc == 'c')
				{
					jtf.copy();
					e.consume();
				}
				else if(kc == 'x')
				{
					jtf.cut();
					e.consume();
				}
				else if(kc == 'v')
				{
					jtf.paste();
					e.consume();
				}
				else if(kc == 'a')
				{
					jtf.selectAll();
					e.consume();
				}
			}
		}
		public void keyPressed(KeyEvent e)
		{}
		public void keyReleased(KeyEvent e)
		{}
	}
	JTextField jtf;
	
	TextThingy theName;
	BackgroundThingy theBack;
	ImageComponent thePicture;
	TextThingy theDescription;
	TextThingy theHappenings;
	JTree theStuff;
	Faucet faucet;
	private JSplitPane mainPane;
	private JSplitPane topPane;
}
