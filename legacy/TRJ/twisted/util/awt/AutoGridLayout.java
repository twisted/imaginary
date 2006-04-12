package twisted.util.awt;
import java.awt.*;
import java.util.Hashtable;

/**
 * This class functions sort of like a cross between
 * <code>java.awt.GridLayout</code> and
 * <code>java.awt.GridBagLayout</code>. Instantiating it creates a
 * layout manager * with a grid of an arbitrary number of
 * cells. Components can take up one or more cells when added to a
 * Container using this layout manager. The bounds of an object are
 * specified * by passing a Rectangle to the constraints argument of
 * add() in Container. Here's an example:
 *
 *	<PRE>
 *		getContentPane().setLayout(new AutoGridLayout(45,30));
 *		setSize(30,30,600,400);
 *		getContentPane().add(myComponent, new Rectangle(0,1,7,2));
 *  </PRE>
 *	
 * This code results in a gridsize of about 12 pixels square. When
 * added, <code>myComponent</code> has bounds of about x=0, y=12,
 * width=84, height=24.
 *
 *	@version 	1.0, 07/21/99
 *	@author		Phil Christensen
 *	@implements	java.awt.LayoutManager2
 */

public class AutoGridLayout implements LayoutManager2
{
	int rows;
	int columns;
	
	int hpad=5;
	int vpad=5;
	
	Hashtable components = new Hashtable(50);
	
	/**
	 * Create a new AutoGridLayout layout manager with an invisible
	 * grid that has <code>columns</code> columns and
	 * <code>rows</code> rows (pretty intuitive, huh? ;-)).
	 *
	 * @param columns number of grid cells across
	 * @param rows number of grid cells down
	 */
	public AutoGridLayout(int columns, int rows,int hpadding, int vpadding)
	{
		this.rows = rows;
		this.columns = columns;
		this.hpad=hpadding;
		this.vpad=vpadding;
	}

	abstract class sizer
	{
		void setComponent(Component c)
		{
			cmp=c;
		}
		Component cmp;
		abstract Dimension size();
	}
	
	class minimumSize extends sizer
	{
		Dimension size()
		{
			return cmp.getMinimumSize();
		}
	}

	class preferredSize extends sizer
	{
		Dimension size()
		{
			return cmp.getPreferredSize();
		}
	}
	
	class maximumSize extends sizer
	{
		Dimension size()
		{
			return cmp.getMaximumSize();
		}
	}
	
	Dimension calculateSize(Container parent,
							sizer s)
	{
		Component[] items=parent.getComponents();
		Dimension myFinalD=new Dimension();
		
		for (int i = 0; i<items.length; i++)
		{
			Component c=items[i];
			Rectangle boundz = (Rectangle) components.get(c);
			s.setComponent(c);
			Dimension dm = s.size();
			dm=s.size();
			dm.width=dm.width/boundz.width;
			dm.height=dm.height/boundz.height;
			if (myFinalD.width<dm.width)
				myFinalD.width=dm.width;
			if (myFinalD.height<dm.height)
				myFinalD.height=dm.height;
		}
		myFinalD.width*=columns;
		myFinalD.height*=rows;
		return myFinalD;
	}
	
	public void layoutContainer(Container parent)
	{
		Component[] items = parent.getComponents();
		int heightMultiplier = parent.getSize().height/rows;
		int widthMultiplier  = parent.getSize().width/columns;
		for(int i = 0; i < items.length; i++)
		{
			if(components.containsKey(items[i]))
			{
				Rectangle bounds = (Rectangle)components.get(items[i]);
				items[i].setBounds((bounds.x * widthMultiplier)+hpad,
								   (bounds.y * heightMultiplier)+vpad,
								   (bounds.width * widthMultiplier)-hpad,
								   (bounds.height * heightMultiplier)-vpad);
			}
		}
	}

	public void addLayoutComponent(String name, Component comp)
	{
		components.put(comp, null);
	}

	public void addLayoutComponent(Component comp, Object rectangle)
	{
		components.put(comp, (Rectangle)rectangle);
	}

	public void removeLayoutComponent(Component comp)
	{
		components.remove(comp);
	}
	
	//what cruft....not all that important, since this is a pretty simple layout
	public Dimension minimumLayoutSize(Container parent)
	{
		// return parent.getSize();
		return calculateSize(parent, new minimumSize());
	}
	public Dimension maximumLayoutSize(Container parent)
	{
		// return parent.getSize();
		return calculateSize(parent, new maximumSize());
	}
	public Dimension preferredLayoutSize(Container parent)
	{
		// return parent.getSize();
		return calculateSize(parent, new minimumSize());
	}
	
	public float getLayoutAlignmentX(Container target){return 0;}
	public float getLayoutAlignmentY(Container target){return 0;}
	public void invalidateLayout(Container target){}
}
