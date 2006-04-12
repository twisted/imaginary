package twisted.util.swing;

import java.awt.*;
import java.awt.event.KeyListener;
import java.awt.event.KeyEvent;
import javax.swing.event.*;
import javax.swing.*;

public class TextThingy extends JPanel implements ChangeListener, KeyListener
{
	/* ewww...gross hack to make the scrollbar go up so it looks nice in macos */
	class InsetScrollPaneLayout extends ScrollPaneLayout
	{		
		public void layoutContainer(Container parent)
		{
			super.layoutContainer(parent);
			JScrollBar v = getVerticalScrollBar();
			if (v != null)
			{
				Dimension d = v.getSize();
				d.height -= 14;
				v.setSize(d);
			}
		}
	}
	
	JScrollPane scroller;
	
	int oldMax = Integer.MAX_VALUE;

	public TextThingy()
	{
		this(false);
	}
	public TextThingy(boolean cornercut)
	{
		this(null, cornercut);
	}
	
	public TextThingy(Component defaultComp)
	{
		this(defaultComp, false);
	}
	public TextThingy(Component defaultComp, boolean cornercut)
	{
		defaultComponent = defaultComp;
		editor = new SpecialJTextArea();
		editor.setEditable(false);
		editor.setLineWrap(true);
		editor.setWrapStyleWord(true);
		scroller = new JScrollPane(editor, JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
		if(cornercut)
		{
			ScrollPaneLayout spl = new InsetScrollPaneLayout();
			scroller.setLayout(spl);
			spl.syncWithScrollPane(scroller);
		}
		setLayout(new BorderLayout());
		editor.addKeyListener(this);
		scroller.getVerticalScrollBar().getModel().addChangeListener(this);
		add("Center",scroller);
		setOpaque(false);
	}
	
	public void stateChanged(ChangeEvent e)
	{
		BoundedRangeModel m = (BoundedRangeModel)e.getSource();
		if(m.getMaximum() != oldMax)
		{
			oldMax = m.getMaximum();
			m.setValue(oldMax);
		}
	}
	
	public void keyTyped(KeyEvent e)
	{
		if(!editor.isEditable() && defaultComponent != null)
		{
			char kc = e.getKeyChar();
			int mod = e.getModifiers();
			if(kc == 'c' && ((mod & KeyEvent.CTRL_MASK) != 0 || (mod & KeyEvent.META_MASK) != 0))
			{
				editor.copy();
				e.consume();
			}
			else if(kc == 'x' && ((mod & KeyEvent.CTRL_MASK) != 0 || (mod & KeyEvent.META_MASK) != 0 ))
			{
				editor.getToolkit().beep();
				e.consume();
			}
			else
			{
				defaultComponent.requestFocus();
				defaultComponent.dispatchEvent(e);
			}
		}
	}
	
	public void keyPressed(KeyEvent e)
	{}
	public void keyReleased(KeyEvent e)
	{}
	public void setText(String s)
	{
		editor.setText(s);
		editor.repaint();
	}

	public void append(String s) 
	{
		editor.append(s);
	}

	public void setFont(Font f) 
	{
		super.setFont(f);
		if (editor != null)
			editor.setFont(f);
	}

	public String getText()
	{
		return editor.getText();
	}

	public void setEditable(boolean tf)
	{
		editor.setEditable(tf);
	}

	public void setColor(Color c)
	{
		editor.setForeground(c);
	}

	JTextArea editor;
	Component defaultComponent;
}


