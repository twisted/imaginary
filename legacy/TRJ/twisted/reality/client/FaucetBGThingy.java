package twisted.reality.client;

import twisted.util.swing.*;
import java.awt.Image;

public class FaucetBGThingy extends BackgroundThingy
{
	protected boolean imageSet = false;
	public FaucetBGThingy()
	{
		super();
	}
	
	public void setImage(Image a)
	{
		if(a == null)
		{
			super.setImage(SwingNozzle.currentTheme+"/dbg");
			imageSet = false;
		} else {
			super.setImage(a);
			imageSet = true;
		}
	}
	public void updateUI()
	{
		super.updateUI();
		if(!imageSet && SwingNozzle.currentTheme != null)
			bg = ImageServer.getImage(SwingNozzle.currentTheme+"/dbg", this);
	}
}
