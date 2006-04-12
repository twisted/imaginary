package twisted.util.swing;

import javax.swing.*;
import javax.swing.text.*;
import java.awt.event.*;
import java.util.*;

public class HistoryTextField extends JTextField implements ActionListener
{
	protected Vector history = new Vector(20);
	protected int historyPos = -1;
	
	public HistoryTextField()
	{
		super();
		
		addActionListener(this);
		
		Keymap map = getKeymap();
		
		map.addActionForKeyStroke(
			KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_UP, 0),
			new AbstractAction()
			{
				public void actionPerformed(ActionEvent e)
				{
					if(historyPos > 0)
						setText((String)history.elementAt(--historyPos));
				}
			});
		
		map.addActionForKeyStroke(
			KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_DOWN, 0),
			new AbstractAction()
			{
				public void actionPerformed(ActionEvent e)
				{
					if(historyPos == history.size())
						setText("");
					else
						setText((String)history.elementAt(historyPos++));
				}
			});		
	}
	
	public void actionPerformed(ActionEvent e)
	{
		if(e.getSource() == this)
		{
			history.addElement(getText());
			historyPos = history.size();
			setText("");
		}
	}
}