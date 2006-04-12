package twisted.util.awt;

import java.awt.*;
import twisted.util.swing.*;

public class SplashScreen extends Window
{
	public SplashScreen (String imagegrab)
	{
		super (new Frame());
		ImageComponent i = new ImageComponent(imagegrab);
		setLayout(new BorderLayout());
		add(i);
		Dimension d = i.getPreferredSize();
		setSize(d.width,d.height);
		d=Toolkit.getDefaultToolkit().getScreenSize();
		setLocation((d.width/2)-(getBounds().width/2),(d.height/2)-(getBounds().height/2));
		setVisible(true);
	}
	
	public static void main(String args[])
	{
		new SplashScreen(args[0]);
	}
}
