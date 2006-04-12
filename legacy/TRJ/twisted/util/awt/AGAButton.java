//package aga;
package twisted.util.awt;
// No package - likely to be UNUSED in future versions...
/*
	AGAButton
	An implementation of the Apple Grayscale Spec.
	David Himelright, 1997
*/

import java.awt.Canvas;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Event;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;

public class AGAButton extends Canvas {

/*
Variable declarations
*/

	String label;
	private boolean selected = false;
	protected boolean enabled = true;
	private int style = 0;
	Font sysFont;
	protected int  minWidth = 10;
/*
Constructors
*/	
	
	//constructor for AGAButton without label
	public AGAButton() {
		this.label = "";
		this.sysFont = new Font("DialogInput",0,12);
	}
	
	//simple constructor for a button with label
	public AGAButton(String label) {
		this.label = label;
		this.sysFont = new Font("DialogInput",0,12);
	}
	
	//constructor allows you to select the font	
	public AGAButton(String label, Font sysFont_) {
		this.label = label;
		this.sysFont = sysFont_;
	}
	
	//creates a "Default" button with border
	public AGAButton(String label, int style_) {
		this.label = label;
		this.sysFont = new Font("DialogInput",0,12);
		this.style = style_;
	}
/*
Methods
*/

	//Gets the label of the button.
	public String getLabel() {
		return label;
	}

	//Sets the button with the specified label.
	public void setLabel(String label) {
		this.label = label;
	}

	//Returns the parameter String of this button.
	protected String paramString() {
		return super.paramString() + ",label=" + label;
	}

	 //yes, you can tab to it
	boolean tabbable() {
	 	return true;
	}

	/**
	 * Enables the button.
	 */
	public synchronized void enable() {
		super.enable();
		enabled = true;
		repaint();
	}

	/**
	 * Disables the button.
	 */
	public synchronized void disable() {
		super.disable();
		enabled = false;
		repaint();
	}

	/**
	 * Called if the mouse is down.
	 */
	public boolean mouseDown(Event evt, int x, int y) {
		// mark as selected and repaint
		selected = true;
		repaint();
		return true;
	}

	/**
	 * Called when the mouse exits the button.
	 */
	public boolean mouseExit(Event evt, int x, int y) {
		if (selected) {
	 // mark as un-selected and repaint
	 selected = false;
	 repaint();
		}
		return true;
	}

	/**
	 * Called if the mouse is up.
	 */
	public boolean mouseUp(Event evt, int x, int y) {
		if (selected) {
	 // mark as un-selected and repaint
	 selected = false;
	 repaint();
	 // generate action event
	 Event event = new Event(this, Event.ACTION_EVENT, (Object) label);
	 deliverEvent(event);
		}
		return true;
	}

	public Dimension preferredSize() {
		return minimumSize();
	}

	public synchronized Dimension minimumSize() {
		Dimension d = new Dimension();
		// get size of label
		FontMetrics fm = getFontMetrics(getFont());
		d.width = Math.max(fm.stringWidth(label) + 22, minWidth);
		d.height = fm.getAscent() + fm.getDescent() + 7;
		return d;
	}

	public void update(Graphics g) {
		paint(g);
	}
/****************************
Various states of AGAButton

enabled=true
	isDefault=true
		selected=true
			label=null
			label=*
		selected=false
			label=null
			label=*
	isDefault=false
enabled=false
	isDefault=true
		label=null
		label=*
	isDefault=false
		label=null
		label=*
****************************/
	public synchronized void paint(Graphics g) {
	
		Dimension size = size();
		
		//fill the background?
		int xSiz = size.width;
		int ySiz = size.height;
		int xPos = (size.width - xSiz) / 2;
		int yPos = (size.height - ySiz) / 2;
		g.setColor(getBackground());
		g.fillRect(xPos, yPos, xSiz + 2, ySiz + 2);
		
		//Set the font to the System face (or the one you passed me)
		g.setFont(sysFont);
		
		if(enabled) {
			if (style == 1) {
				if (selected) {
					paintOuter(g, size);
					paintInnerSelected(g, size);
					paintLabel(g, size, Color.white);
					}
				else {
					paintOuter(g, size);
					paintInner(g, size);
					paintLabel(g, size, Color.black);
					}
			}
			else if (style == 2) {
				if (selected) {
					paintInnerSelected(g, size);
					paintLabel(g, size, Color.white);
					}
				else {
					paintInner(g, size);
					paintLabel(g, size, Color.black);
					}
			}
			else		
				if (selected) {
					paintSelected(g, size);
					paintLabel(g, size, Color.white);
					}
				else {
					paintButton(g, size);
					paintLabel(g, size, Color.black);
					}
			}
		else {
			if (style == 1) {
				paintOuterDisabled(g, size);
				paintInnerDisabled(g, size);
				paintLabel(g, size, new Color(136,136,136));
			}
			else if (style == 2) {
				paintInnerDisabled(g, size);
				paintLabel(g, size, new Color(136,136,136));
			}
			else {
				paintDisabled(g, size);
				paintLabel(g, size, new Color(136,136,136));
			}
		}
	}

//Paint the button as selected

	public synchronized void paintSelected(Graphics g, Dimension size) {
		g.setColor( new Color( 102,102,102 ) );
		g.fillRoundRect( 0,0, size.width, size.height,8,8);
		g.setColor( Color.black );
		g.drawRoundRect( 0, 0, size.width-1, size.height-1,8,8 );
		g.setColor( new Color( 85,85,85 ) );
		g.drawLine( 2,2,size.width-4,2 );
		g.drawLine( 3,3,3,3 );
		g.drawLine( 2,2,2,size.height-4 );
		g.setColor( new Color( 68,68,68 ) );
		g.drawLine( 2,1,size.width-3,1 );
		g.drawLine( 1,2,1,size.height-3 );
		g.drawLine( 2,2,2,2 );
		g.setColor( new Color( 119,119,119 ) );		
		g.drawLine( 3,size.height-3,size.width-3,size.height-3 );
		g.drawLine( size.width-3,3,size.width-3, size.height-3 );
		g.drawLine( size.width-2,2,size.width-2,2 );
		g.drawLine( size.width-4,size.height-4,size.width-4,size.height-4 );
		g.drawLine( 2,size.height-2,2,size.height-2 );
		g.setColor( new Color(136,136,136 ) );
		g.drawLine( 3,size.height-2,size.width-3,size.height-2 );
		g.drawLine( size.width-2,3,size.width-2,size.height-3 );
		g.drawLine( size.width-3,size.height-3,size.width-3,size.height-3 );
		g.setColor( new Color( 34,34,34 ) );
		g.drawLine( size.width-3,0,size.width-3,0 );	
		g.drawLine( size.width-1,2,size.width-1,2 );
		g.drawLine( size.width-3,size.height-1,size.width-3,size.height-1 );
		g.drawLine( size.width-1,size.height-3,size.width-1,size.height-3 );
		g.drawLine( 0,size.height-3,0,size.height-3 );
		g.drawLine( 2,size.height-1,2,size.height-1 );
		g.drawLine( 0,2,0,2 );
		g.drawLine( 2,0,2,0 );
	}
//Paint the button
	public synchronized void paintButton(Graphics g, Dimension size) {
		g.setColor( new Color( 221,221,221 ) );
		g.fillRoundRect( 0,0, size.width-1, size.height-1,10,10);
		g.setColor( Color.black );
		g.drawRoundRect( 0, 0, size.width-1, size.height-1,10,10 );
		g.setColor( Color.white );
		g.drawLine( 2,2,size.width-4,2 );
		g.drawLine( 3,3,3,3 );
		g.drawLine( 2,2,2,size.height-4 );
		g.setColor( new Color( 170,170,170 ) );		
		g.drawLine( 3,size.height-3,size.width-3,size.height-3 );
		g.drawLine( size.width-3,3,size.width-3, size.height-3 );
		g.drawLine( size.width-3,1, size.width-3,1 );
		g.drawLine( size.width-2,2,size.width-2,2 );
		g.drawLine( 2,1,2,1 );
		g.drawLine( 1,2,1,2 );
		g.drawLine( 1,size.height-3,1,size.height-3 );
		g.drawLine( 2,size.height-2,2,size.height-2 );
		g.drawLine( size.width-4,size.height-4,size.width-4,size.height-4 );
		g.setColor( new Color( 119,119,119 ) );
		g.drawLine( 3,size.height-2,size.width-3,size.height-2 );
		g.drawLine( size.width-2,3,size.width-2,size.height-3 );
		g.drawLine( size.width-3,size.height-3,size.width-3,size.height-3 );
		g.setColor( new Color( 34,34,34 ) );
		g.drawLine( size.width-3,0,size.width-3,0 );	
		g.drawLine( size.width-1,2,size.width-1,2 );
		g.drawLine( size.width-3,size.height-1,size.width-3,size.height-1 );
		g.drawLine( size.width-1,size.height-3,size.width-1,size.height-3 );
		g.drawLine( 0,size.height-3,0,size.height-3 );
		g.drawLine( 2,size.height-1,2,size.height-1 );
		g.drawLine( 0,2,0,2 );
		g.drawLine( 2,0,2,0 );
	}

	private synchronized void paintDisabled(Graphics g, Dimension size) {
		g.setColor( new Color( 221,221,221 ) );
		g.fillRoundRect( 0,0, size.width, size.height,8,8);
		g.setColor( new Color( 136,136,136 ) );
		g.drawRoundRect( 0, 0, size.width-1, size.height-1,8,8 );
	}
	
	private synchronized void paintDefault(Graphics g, Dimension size) {
		paintOuter(g,size);
		paintInner(g,size);
		paintLabel(g,size,Color.black);
	}

	private synchronized void paintDefaultSelected(Graphics g, Dimension size) {
		paintOuter(g,size);
		paintInnerSelected(g,size);
		paintLabel(g,size,Color.white);
	}
	
	private synchronized void paintOuterDisabled(Graphics g, Dimension size) {
		g.setColor( new Color( 221,221,221 ) );
		g.fillRoundRect( 0,0, size.width, size.height,11,11);
		g.setColor( new Color( 136,136,136 ) );
		g.drawRoundRect( 0, 0, size.width-1, size.height-1,11,11 );		
	}
	
	private synchronized void paintInnerDisabled(Graphics g, Dimension size) {
		g.setColor( new Color( 221,221,221 ) );
		g.fillRoundRect( 3, 3, size.width-7, size.height-7,8,8 );
		g.setColor( new Color( 136,136,136 ) );
		g.drawRoundRect( 3, 3, size.width-7, size.height-7,8,8 );	
	}
	
	private synchronized void paintOuter(Graphics g, Dimension size) {
		g.setColor( new Color( 221,221,221 ) );
		g.fillRoundRect( 0,0, size.width-1, size.height-1,11,11);
		g.setColor( Color.black );
		g.drawRoundRect( 0,0, size.width-1, size.height-1,11,11 );
		g.setColor( Color.white );
		g.setColor( new Color( 170,170,170 ) );	
		g.fillRoundRect(2,2,size.width-4,size.height-4,8,8);
		g.setColor( new Color( 119,119,119 ) );
		g.drawLine(size.width-2,4,size.width-2,size.height-4);
		g.drawLine(4,size.height-2,size.width-4,size.height-2);
		g.drawLine(size.width-3,size.height-4,size.width-3,size.height-3);
		g.drawLine(size.width-4,size.height-3,size.width-4,size.height-3);
		g.setColor( new Color( 34,34,34 ) );
		g.drawLine(0,3,0,3);
		g.drawLine(3,0,3,0);
		g.drawLine(0,size.height-4,0,size.height-4);
		g.drawLine(3,size.height-1,3,size.height-1);
		g.drawLine(size.width-1,size.height-4,size.width-1,size.height-4);
		g.drawLine(size.width-4,size.height-1,size.width-4,size.height-1);
		g.drawLine(size.width-4,0,size.width-4,0);
		g.drawLine(size.width-1,3,size.width-1,3);
	}
	
	private synchronized void paintInner(Graphics g, Dimension size) {
		g.setColor( new Color( 221,221,221 ) );
		g.fillRoundRect( 3,3, size.width-7, size.height-7,8,8);
		g.setColor( Color.black );
		g.drawRoundRect( 3,3, size.width-7, size.height-7,8,8 );
		g.setColor( Color.white );
		g.drawLine( 5,5,size.width-7,5 );
		g.drawLine( 6,6,6,6 );
		g.drawLine( 5,5,5,size.height-7 );
		g.setColor( new Color( 170,170,170 ) );		
		g.drawLine( 6,size.height-6,size.width-6,size.height-6 );
		g.drawLine( size.width-6,6,size.width-6, size.height-6 );
		g.drawLine( size.width-6,4, size.width-6,4 );
		g.drawLine( size.width-5,5,size.width-5,5 );
		g.drawLine( 5,4,5,4 );
		g.drawLine( 4,5,4,5 );
		g.drawLine( 4,size.height-6,4,size.height-6 );
		g.drawLine( 5,size.height-5,5,size.height-5 );
		g.drawLine( size.width-7,size.height-7,size.width-7,size.height-7 );
		g.setColor( new Color( 119,119,119 ) );
		g.drawLine( 6,size.height-5,size.width-6,size.height-5 );
		g.drawLine( size.width-5,6,size.width-5,size.height-6 );
		g.drawLine( size.width-6,size.height-6,size.width-6,size.height-6 );
		g.setColor( new Color( 34,34,34 ) );
		g.drawLine( size.width-6,3,size.width-6,3 );	
		g.drawLine( size.width-4,5,size.width-4,5 );
		g.drawLine( size.width-6,size.height-4,size.width-6,size.height-4 );
		g.drawLine( size.width-4,size.height-6,size.width-4,size.height-6 );
		g.drawLine( 3,size.height-6,3,size.height-6 );
		g.drawLine( 5,size.height-4,5,size.height-4 );
		g.drawLine( 3,5,3,5 );
		g.drawLine( 5,3,5,3 );
	}

	private synchronized void paintInnerSelected(Graphics g, Dimension size) {
		g.setColor( new Color( 102,102,102 ) );
		g.fillRoundRect( 3,3, size.width-7, size.height-7,8,8);
		g.setColor( Color.black );
		g.drawRoundRect( 3,3, size.width-7, size.height-7,8,8 );
		g.setColor( new Color( 85,85,85 ) );
		g.drawLine( 5,5,size.width-7,5 );
		g.drawLine( 6,6,6,6 );
		g.drawLine( 5,5,5,size.height-7 );
		g.setColor( new Color( 68,68,68 ) );
		g.drawLine( 5,4,size.width-6,4 );
		g.drawLine( 4,5,4,size.height-6 );
		g.drawLine( 5,5,5,5 );
		g.setColor( new Color( 119,119,119 ) );		
		g.drawLine( 6,size.height-6,size.width-6,size.height-6 );
		g.drawLine( size.width-6,6,size.width-6, size.height-6 );
		g.drawLine( size.width-5,5,size.width-5,5 );
		g.drawLine( size.width-7,size.height-7,size.width-7,size.height-7 );
		g.drawLine( 5,size.height-5,5,size.height-5 );
		g.setColor( new Color(136,136,136 ) );
		g.drawLine( 6,size.height-5,size.width-6,size.height-5 );
		g.drawLine( size.width-5,6,size.width-5,size.height-6 );
		g.drawLine( size.width-6,size.height-6,size.width-6,size.height-6 );
		g.setColor( new Color( 34,34,34 ) );
		g.drawLine( size.width-6,3,size.width-6,3 );	
		g.drawLine( size.width-4,5,size.width-4,5 );
		g.drawLine( size.width-6,size.height-4,size.width-6,size.height-4 );
		g.drawLine( size.width-4,size.height-6,size.width-4,size.height-6 );
		g.drawLine( 3,size.height-6,3,size.height-6 );
		g.drawLine( 5,size.height-4,5,size.height-4 );
		g.drawLine( 3,5,3,5 );
		g.drawLine( 5,3,5,3 );
	}
	
	private synchronized void paintLabel(Graphics g, Dimension size, Color c) {
		g.setColor(c);
		int labelX = 0;
		int labelY = 0;
		int labelW = 0;
		int labelH = 0;
		FontMetrics fm = null;
		Font f = sysFont;
		fm = getFontMetrics(f);
		labelH = fm.getAscent() + fm.getDescent();
		labelW = fm.stringWidth(label);
		labelX = size.width/2 - labelW/2;
		labelY = size.height/2 - labelH/2 + fm.getAscent() -1;
		g.drawString(label,  labelX, labelY);
	}
}

