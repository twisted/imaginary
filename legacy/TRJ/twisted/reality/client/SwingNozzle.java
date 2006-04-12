package twisted.reality.client;

import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.*;
import java.util.*;
import twisted.util.awt.*;
import twisted.util.swing.*;
import twisted.util.*;
import javax.swing.*;
import javax.swing.text.JTextComponent;
import javax.swing.text.DefaultEditorKit;
import javax.swing.plaf.metal.MetalLookAndFeel;
import javax.swing.text.Keymap;
import com.apple.mrj.*;
import javax.swing.tree.*;


public class SwingNozzle implements MRJQuitHandler, Nozzle//, ListListener
{
/*	public void listUpdated(ThingList tl)
	{
		Enumeration e = tl.elements();
		StringBuffer st = new StringBuffer();
		while(e.hasMoreElements())
		{
			st.append(e.nextElement());
			st.append("\n");
		}
		if (gameWin != null)
		setTextLater (gameWin.theStuff,st.toString());
	}*/
	
	public void logout()
	{
		if(!isQuitting)
		{
			gameWin.setVisible(false);
			loginWin.setVisible(true);
			gameWin.dispose();
			gameWin=null;
		}
	}
	
	Hashtable items = new Hashtable();
	public void addItem(final String item, final String container, final String desc)
	{
		SwingUtilities.invokeLater(new Runnable() { public void run() {
			DefaultMutableTreeNode parent;
			DefaultTreeModel m = (DefaultTreeModel)gameWin.theStuff.getModel();
			parent = (DefaultMutableTreeNode)items.get(container);
			if(parent == null)
				parent = (DefaultMutableTreeNode)m.getRoot();
			
			if(items.containsKey(item))
			{
				System.out.println("Autoremove");
				removeItemInt(item, null);
			}
			DefaultMutableTreeNode n = new DefaultMutableTreeNode(desc);
			items.put(item, n);
			System.out.println("Adding item "+item+" with parent "+container+" with desc " +desc);
			m.insertNodeInto(n, parent, parent.getChildCount());

//			System.out.println("Root visible: " + gameWin.theStuff.isExpanded(new TreePath(m.getRoot())));
//			System.out.println("Node visible: " + gameWin.theStuff.isVisible(new TreePath(n)));
			gameWin.theStuff.expandPath(new TreePath(parent));
			gameWin.theStuff.expandPath(new TreePath(n));
		}});
		//tl.putThing(item,desc);
	}
	private void removeItemInt(String item, String container)
	{
		DefaultMutableTreeNode n = (DefaultMutableTreeNode)items.get(item);
		if(n == null)
		{
			System.out.println("BUG: item "+item+" with parent "+container+" does not exist!");
			return;
		}
		items.remove(item);
		System.out.println("Removing item "+item+" with parent "+container);
		((DefaultTreeModel)gameWin.theStuff.getModel()).removeNodeFromParent(n);
		//tl.remove(item);
	}
	public void removeItem(final String item, final String container)
	{
		SwingUtilities.invokeLater(new Runnable() { public void run() {
			removeItemInt(item, container);
		}});
		//tl.remove(item);
	}
	public void enterItem(final String item, final String container, final String desc)
	{
		new Thread() { public void run() {
			addItem("+"+item, container ,"+++ <"+desc+">");
			try{ Thread.sleep(8000); } catch (Exception e) {}
			removeItem("+"+item,container);
		}}.start();
		//tl.putAdd(item,desc);
	}
	public void leaveItem(final String item, final String container, final String desc)
	{
		new Thread() { public void run() {
			addItem("-"+item, container,"--- ("+desc+")");
			try{ Thread.sleep(8000); } catch (Exception e) {}
			removeItem("-"+item,container);
		}}.start();
		//tl.putRem(item,desc);
	}
	public void clearItems()
	{
		System.out.println("Clearing Item List");
		items.clear();
		
		DefaultTreeModel model = (DefaultTreeModel)gameWin.theStuff.getModel();
		((DefaultMutableTreeNode)model.getRoot()).removeAllChildren();
//		gameWin.theStuff.expandPath(new TreePath(model.getRoot()));
		model.reload();
//		System.out.println("Root visible: " + gameWin.theStuff.isExpanded(new TreePath(model.getRoot())));
/*		tl.setListListener(null);
		tl=new ThingList();
		tl.setListListener(this);*/
	}
	
	public void completeAction()
	{
		/* set enabled or something */
		try
		{
		SwingUtilities.invokeAndWait
			(new Runnable()
		{
			public void run()
			{
				gameWin.jtf.setText("");
				gameWin.jtf.setEnabled(true);
				gameWin.jtf.requestFocus();
			}
		});
		}
		catch(InterruptedException ie) {}
		catch(java.lang.reflect.InvocationTargetException ie) {}
	}
	
	public void handleError(Throwable t)
	{
		StringWriter sw = new StringWriter();
		PrintWriter pw = new PrintWriter(sw);
		
		t.printStackTrace(pw);
		dialog(sw.toString());
	}
	public static boolean isMacOS;
	
//	ThingList tl;
	public SwingNozzle()
	{
		isMacOS = (System.getProperty("os.name")).startsWith("Mac");
		setTheme("default");
		MRJApplicationUtils.registerQuitHandler(this);
		final SwingNozzle realThis=this;

		try{
			SwingUtilities.invokeAndWait(new Runnable() {
			public void run() {
				loginWin = new LoginDialog(realThis);
				loginWin.setVisible(true);
//				tl=new ThingList();
//				tl.setListListener(realThis);
		}});}
		catch(Exception e){}
		
/*	I really have *NO* idea why this doesn't work properly...It does the action, but it ALSO
	inserts the character (c v x or a), which makes it completely useless. As far as I can tell
	the swing code claims it should be consuming the event if an action occurs, but apparently
	that doesn't actually work right. Therefore I do the equivilent of the following with
	a KeyListener, which actually *DOES* work.
		final JTextComponent.KeyBinding[] defaultBindings = {
		   new JTextComponent.KeyBinding(
		   KeyStroke.getKeyStroke(KeyEvent.VK_C, InputEvent.META_MASK),
		   DefaultEditorKit.copyAction),
		   new JTextComponent.KeyBinding(
		   KeyStroke.getKeyStroke(KeyEvent.VK_V, InputEvent.META_MASK),
		   DefaultEditorKit.pasteAction),
		   new JTextComponent.KeyBinding(
		   KeyStroke.getKeyStroke(KeyEvent.VK_X, InputEvent.META_MASK),
		   DefaultEditorKit.cutAction),
		   new JTextComponent.KeyBinding(
		   KeyStroke.getKeyStroke(KeyEvent.VK_A, InputEvent.META_MASK),
		   DefaultEditorKit.selectAllAction),		   
		   };
		JTextComponent c = new JTextField();
		Keymap k = c.getKeymap(JTextComponent.DEFAULT_KEYMAP);
		c.loadKeymap(k, defaultBindings, c.getActions());*/
	}
	
	public static Font font = new Font ("Courier",Font.BOLD,12);
	
	/* attempt to print a more meaningful error message if swing isn't installed than "NoClassDefFoundError" */
	static
	{

		try
		{
			Class c = Class.forName("javax.swing.SwingUtilities");
		}
		catch (ClassNotFoundException e)
		{
			System.out.println("FATAL ERROR: Swing is required for this program to run.");
			System.out.println("  Please make sure it is installed and that your classpath is set properly.");
			throw new RuntimeException();
		}
		ImageServer.imagePath="images";
	}
	
	public void handleQuit()
	{
		if(gameWin != null && gameWin.faucet != null)
		{
			isQuitting = true;
			if(gameWin != null && gameWin.faucet != null)
				gameWin.faucet.bye();
		}
		if(isMacOS)
		{
			Window window = new Window(loginWin);
			window.setBounds(-500, -500, -400, -400);
			window.show();
		}
		System.exit(0);
	}
	
	public void hears(String aPhrase)
	{
		final String aa=aPhrase;
		SwingUtilities.invokeLater(new Runnable()
		{
			public void run()
			{
				gameWin.theHappenings.append("\n"+aa);
			}
		});
	}
	
	public void sees(String aGraphic)
	{
		// gameWin.thePicture.setImage(aGraphic);
	}
	
	public void setTheme(String s)
	{
		SwingUtilities.invokeLater(new ThemeSetter(s));
	}
	
	class ThemeSetter implements Runnable
	{
		String s;
		public ThemeSetter(String xx)
		{
			s=xx;
		}
		public void run() 
		{
			if (s.equals(currentTheme))
				return;
			
			try
			{
				if("builtin".equals(s))
				{
					MetalLookAndFeel.setCurrentTheme(new FTheme());
				}
				else
				{
					InputStream f = getClass().getResourceAsStream("/images/"+s+"/colors.txt");
					if(f == null)
					{
						System.out.println("Theme " + s + " nonexistant!");
						if("default".equals(s))
							setTheme("builtin");
						else
							setTheme("default");
						return;
					}
					BufferedReader d = new BufferedReader(new InputStreamReader(f));
					Color wh = ColorGenerator.createColor(d.readLine());
					Color bk = ColorGenerator.createColor(d.readLine());
					Color p1 = ColorGenerator.createColor(d.readLine());
					Color p2 = ColorGenerator.createColor(d.readLine());
					Color p3 = ColorGenerator.createColor(d.readLine());
					Color s1 = ColorGenerator.createColor(d.readLine());
					Color s2 = ColorGenerator.createColor(d.readLine());
					Color s3 = ColorGenerator.createColor(d.readLine());
					
					MetalLookAndFeel.setCurrentTheme(new FTheme(wh,bk,p1,p2,p3,s1,s2,s3));
					currentTheme=s;
				}
				try
				{
					UIManager.setLookAndFeel("javax.swing.plaf.metal.MetalLookAndFeel");
					if (gameWin != null)
						SwingUtilities.updateComponentTreeUI(gameWin.getContentPane());
					if (loginWin != null)
						SwingUtilities.updateComponentTreeUI(loginWin.getContentPane());
				}
				catch (Exception e)
				{
					currentTheme="000";
					System.out.println(e);
					e.printStackTrace();
					System.out.println("Oh NO!!! Something has gone HORRIBLY WRONG!!!:");
				}
			}
			catch(Exception e)
			{
				System.out.println("Error setting theme to " + s + ".");
				e.printStackTrace();
				if("default".equals(s))
					setTheme("builtin");
				else
					setTheme("default");
				return;
			}
			SwingUtilities.invokeLater(new Runnable() { public void run () {
				if (gameWin != null)
				{
					gameWin.requestFocus();
					gameWin.jtf.requestFocus();
				}
			}});
		}
	}

	public void setName(Vector nm)
	{
		StringBuffer s = new StringBuffer();
		boolean isFirst = true;
		
		for(Enumeration e = nm.elements(); e.hasMoreElements(); )
		{
			if(isFirst)
				isFirst=false;
			else
				s.insert(0, ":");
			s.insert(0, e.nextElement());
		}
		String sts = s.toString();
		setTitleLater(gameWin,"Reality Faucet - "+sts);
		setTextLater(gameWin.theName, sts);
	}
	
	public void setDescription(String s)
	{
		__descr__=s;
		
		updateDescription();
	}
	
	public void updateDescription()
	{
		setTextLater(gameWin.theDescription,__descr__+__exits__);
	}
	static SplashScreen begin;
	public static void main(String[] args)
	{
		begin = new SplashScreen("trl");
		theIcon=ImageServer.getImage("faucet",begin);
		new SwingNozzle();
		begin.dispose();
	}
	  					
	public void setTitleLater(final JFrame jf, final String text)
	{
		if (jf != null)
			SwingUtilities.invokeLater(new Runnable() {
				public void run()
				{
					jf.setTitle(text);
				}
			});
	}
	
	public void setTextLater(final TextThingy jtc, final String text)
	{
		if (jtc != null)
			SwingUtilities.invokeLater(new Runnable() { public void run() {
				jtc.setText(text);
				
				// This is a kludge, but it appears to improve some
				// really erratic performance on Linux.  Please don't
				// remove this.
				
				gameWin.jtf.requestFocus();
			}});
		
	}
	
	public void dialog(final String s)
	{
		SwingUtilities.invokeLater(new Runnable() {
			public void run()
			{
				new JAnswerDialog(s,loginWin);
			}
		});
	}
	
	public void requestResponse(String a, String b, String c)
	{
		if (gameWin != null)
			gameWin.requestResponse(a,b,c);
	}

	public void setExits(Vector ex)
	{
		/* Note: vector ex must be duplicated if its ever stored here */
		
		StringBuffer s = new StringBuffer("\nObvious Exits: ");
		boolean isFirst = true;
		
		for (Enumeration e = ex.elements(); e.hasMoreElements(); )
		{
			if(isFirst)
				isFirst=false;
			else
				s.append(", ");
			s.append(e.nextElement());
		}
		__exits__ = s.toString();
		updateDescription();
	}
	
	public GameWindow gameWin;
	public LoginDialog loginWin;
	static String currentTheme;
	static Image theIcon;
	String __exits__;
	String __descr__;
	boolean isQuitting = false;
}
