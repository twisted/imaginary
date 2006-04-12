
package twisted.util.awt;
import java.awt.*;
import java.awt.event.*;
public class TextDisplayWindow extends Frame implements WindowListener
{
	public TextDisplayWindow(String str)
	{
		super(str);
		t=new TextArea(str,20,20,TextArea.SCROLLBARS_VERTICAL_ONLY);
		addWindowListener(this);
		t.setEditable(false);
		setLayout(new BorderLayout());
		add("Center",t);
		setSize(250,320);
	}	
	
	public void windowActivated(WindowEvent e) {}
	
	public void windowClosed(WindowEvent e) {}
	
	public void windowClosing(WindowEvent e) 
	{
		setVisible(false);
	}
	
	public void windowDeactivated(WindowEvent e) {}
	
	public void windowDeiconified(WindowEvent e) {}
	
	public void windowIconified(WindowEvent e) {}
	
	public void windowOpened(WindowEvent e) {}
	
	public void setText(String str)
	{
		mstr=str;
		t.setText(mstr);
	}	
	
	protected String mstr;
	
	protected TextArea t;
}
