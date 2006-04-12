package demo;

import twisted.reality.*;

public class ScreenSaverOn extends RealEventHandler
{
	public void gotEvent(RealEvent e, Thing keyboard)
	{
		Thing monitor = keyboard.getThing("monitor");
		monitor.putDescriptor("screen", "In the background, a screensaver is tracing out some trippy mathematical figures, and an \"Enter Password:\" window is open in the center of the screen, displaying an empty password field.");
		keyboard.putString("entry", "");
		try
		{
			keyboard.removeVerb("demo.DemoComputerLocked");
		}
		catch (ClassNotFoundException cnfe){}
		try
		{
			keyboard.addVerb("demo.DemoComputerType");
		}
		catch (ClassNotFoundException cnfe){}
	}
}
