package twisted.util.swing;

import java.util.*;
import java.awt.*;
import javax.swing.*;
import javax.swing.tree.*;
import javax.swing.plaf.metal.MetalTreeUI;
import javax.swing.plaf.basic.BasicTreeUI;

/*
  Okay, most of this (very hacky) code depends _HEAVILY_ on the internals of JTree.
  That is bad programming practice, but they have left me no choice if this is going
  to work.
 */

public class WrappableJTree extends JTree
{
	/* What the @@#$ were they smoking when they made the default constructor for JTree?
	   Returns a "sample model"?? Its useful for an example in BeanBox? YAY???
	   I refuse to have a default constructor that useless.
	   Now for a SENSIBLE default constructor..
	 */
	public WrappableJTree()
	{
		super(new DefaultMutableTreeNode());
		this.setRootVisible(false);
		this.setShowsRootHandles(true);
	}
	/* Yay constructors... */
	public WrappableJTree(Object[] value) {
		super(value);
	}
	public WrappableJTree(Vector value) {
		super(value);
	}
	public WrappableJTree(Hashtable value) {
		super(value);
	}
	public WrappableJTree(TreeNode root) {
		super(root);
	}
	public WrappableJTree(TreeNode root, boolean asksAllowsChildren) {
		super(root, asksAllowsChildren);
	}
	public WrappableJTree(TreeModel newModel) {
		super(newModel);
	}

	/* JTree: "Only expand if not leaf!"
	   NO!!!! Don't only expand if leaf you stupid POS. If I tell you to expand
	   it, I _meant_ it, even if i haven't added the other items yet!
	   **WHACK**... hey it still doesn't work. **POUT**
	 */
/*	public void expandPath(TreePath path)
	{
		if(path != null)
		{
			setExpandedState(path, true);
		}
	}*/

	/* Don't you love the way they try to make it practically impossible to
	   keep the UI you assigned to a component?
	 */
	HackTreeUI hackUI = null;
	public void updateUI()
	{
		if(hackUI == null)
			hackUI = new HackTreeUI();
		setUI(hackUI);
		invalidate();
	}
	
	public boolean getScrollableTracksViewportWidth()
	{
		return true;
	}
	
	/* Swing sucks and doesn't believe that the row's sizes could change
	   if the width of the tree changes... **WHACK**... ahh much better.
	 */
	public void reshape(int x, int y, int width, int height)
	{
		super.reshape(x,y,width,height);
		HackTreeUI ui= (HackTreeUI)getUI();
		ui.invalidateSizes();
	}

	/* It'd be nice if java had categories so that I didn't have to assume
	   we were using the Metal theme, but it doesn't, so suffer.
	 */
	class HackTreeUI extends MetalTreeUI
	{
		protected int getNodeDimensionsCurrentX;
		
		/* Okay, pop quiz:
		   Q: why is getNodeDimensions in a seperate class and not in the TreeUI?
		   A: the swing designers didn't know about interfaces!
		      (AbstractLayoutCache.NodeDimensions should be an interface, not a class)
		   A: (also acceptabe) the swing designers were high when they wrote it.
		 */
		/* All this mess is needed so that the CellRenderer can know how much 
		   horizontal screen real estate it has to work with in order to properly
		   respond to getPreferredSize. To know that it has to know where it starts
		   drawing on the X axis, which it can't know until AFTER the getPreferredSize..
		   **WHACK**... ahh much better.
		 */
		public class NodeDimensionsHandler extends BasicTreeUI.NodeDimensionsHandler
		{
			public Rectangle getNodeDimensions(Object value, int row, int depth,
												boolean expanded, Rectangle size)
			{
				getNodeDimensionsCurrentX = getRowX(row, depth);
				return super.getNodeDimensions(value, row, depth, expanded, size);
			}
		}
		
		protected AbstractLayoutCache.NodeDimensions createNodeDimensions()
		{
			return new NodeDimensionsHandler();
		}
		
		public void invalidateSizes()
		{
			if(treeState != null)
				treeState.invalidateSizes();
			updateSize();
/*			validCachedPreferredSize = false;
			tree.treeDidChange();*/
		}
		
		/* Isn't that a nice name? I thought so. :) */
		public int getGetNodeDimensionsCurrentX()
		{
			return getNodeDimensionsCurrentX;
		}
	}
}
