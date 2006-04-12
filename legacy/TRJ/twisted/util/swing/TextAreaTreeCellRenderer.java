package twisted.util.swing;

import javax.swing.*;
import javax.swing.plaf.FontUIResource;
import java.awt.*;
import javax.swing.tree.*;

/* Requires a WrappableJTree tree to work. */
public class TextAreaTreeCellRenderer extends JTextArea implements TreeCellRenderer
{
	protected boolean selected;
	private boolean hasFocus;

	/** Foreground color when selected. */
	protected Color textSelectionColor;

	/** Foreground color when not selected. */
	protected Color textNonSelectionColor;

	/** Background color when selected. */
	protected Color backgroundSelectionColor;

	/** Border color when focused. */
	protected Color borderSelectionColor;

	public TextAreaTreeCellRenderer()
	{
		setOpaque(false);
		setLineWrap(true);
		setWrapStyleWord(true);
		textSelectionColor = UIManager.getColor("Tree.selectionForeground");
		textNonSelectionColor = UIManager.getColor("Tree.textForeground");
		backgroundSelectionColor = UIManager.getColor("Tree.selectionBackground");
		borderSelectionColor = UIManager.getColor("Tree.selectionBorderColor");
	}

	/**
	 * Only accept the font if it isn't a FontUIResource.
	 */
	public void setFont(Font font) {
		if(font instanceof FontUIResource)
		    font = null;
		super.setFont(font);
	}


	/* Sets up this component for a specific row */
	public Component getTreeCellRendererComponent(JTree tree, Object value,
						  boolean selected,
						  boolean expanded,
						  boolean leaf, int row,
						  boolean hasFocus)
	{
		WrappableJTree.HackTreeUI ui = (WrappableJTree.HackTreeUI)tree.getUI();
		Insets i = tree.getInsets();
		
		setEnabled(tree.isEnabled());
		this.hasFocus = hasFocus;
		this.selected = selected;
		//	System.out.println("getTreeCellRendererComponent: tree width " + tree.getWidth() + "offset: " + (ui.getGetNodeDimensionsCurrentX() - tree.getX()));
		
		/*	setSize is needed even though the component will get reshaped again so that the
			JTextArea will know where to wrap and so the getPreferredSize will return the
			correct height. Yes, the height of 20 here is arbitrary, Swing just needs _a_
			height set (greater than the insets) or else it will ignore the width! **WHY?**
		*/
		setSize(tree.getWidth() - i.right -
				(ui.getGetNodeDimensionsCurrentX() - tree.getX() + i.left), 20);
		
		setText(value.toString());
		
		if(selected)
			setForeground(textSelectionColor);
		else
			setForeground(textNonSelectionColor);
		
		return this;
	}

	public void paint(Graphics g)
	{
		if(selected)
		{
			Color bColor = backgroundSelectionColor;
			if(bColor != null)
			{
				g.setColor(bColor);
				g.fillRect(0, 0, getWidth() - 1, getHeight());
			}
		}
		if (hasFocus)
		{
			g.setColor(borderSelectionColor);
			g.drawRect(0, 0, getWidth() - 1, getHeight() - 1);
		}
		super.paint(g);
	}

	/**
	 * Overrides <code>JComponent.getPreferredSize</code> to
	 * return slightly taller preferred size value.
	 */
	public Dimension getPreferredSize()
	{
		Dimension dim = super.getPreferredSize();
		//	System.out.println("getPreferredSize: Requested dim = "+retDimension + "Text: " +getText());
		if(dim != null)
			dim.height += 2;
		return dim;
	}

	// WTF is swing's problem with letting things stay transparent???
	public void setOpaque(boolean b)
	{
		super.setOpaque(false);
	}
}
