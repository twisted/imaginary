/*
  A component which	 displays an Image.
  Copyright (C) 1997  Martin Vogt
  
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation.
  
  For more information visit www.fsf.org
  
*/



// package de.unikl.util;

package twisted.util.swing;

import java.awt.*;
import java.awt.event.*;
import java.lang.*;

/**
 * A Component which displays an Image.
 * Note: The componets gets fully loaded before its displayed
 * 
 * we use a static variable to specify the search path for images
 * 
 * 
 * @author	   Martin Vogt
 * @version	   0.2, 2 Jun 1997
 */





public class ImageComponent extends Component {
	
	
	
	
	/**
	 * The image.
	 */
	
	Image image;
	
	
	
	/**
	 * Name of the filename of the image
	 */
	
	String filename;
	
	
	/**
	 * a descriptive Name for the image
	 */
	
	String metaName;
	
	/**
	 * we store whether this class is painted or not if we call the
	 * paint method.
	 * default is lpainted=true
	 */
	boolean lPaint=true;
	
	/**
	 * The ImageComponent must store the Popupmenu for the images because
	 * if there are two different images (one for open one for close)
	 * and the image change (are removed from the Container) the
	 * Popupmenu would get lost.
	 * Thus it must be stored here
	 */
	
	PopupMenu popup;
	
	/**
	 * Constructs a new ImageComponent.
	 * The image is specified with its filename
	 * @param filename the filename of the image
	 *
	 */
	public ImageComponent (String filename) {
		this(filename,filename);
	}
	
	
	
	/**
	 * Constructs a new ImageComponent.
	 * The image is specified with its filename
	 * @param metaName a description for what the image is used for (eg: "open")
	 * @param filname the filename of the image
	 *
	 */
	public ImageComponent (String metaName, String filename) {
		this.metaName=metaName;
		setImage(filename);
	}
	
	
	
	/**
	 * adds Popupmenu to this Component and enables Mouseevent
	 * @param popup the Popupmenu for this ImageComponent
	 */
	public void add(PopupMenu popup) {
		if (popup != null) {
			this.popup=popup;
			super.add(popup);
			enableEvents(AWTEvent.MOUSE_EVENT_MASK);
		}
	}
	
	
	
	/**
	 * Returns th associated PopupMenu.
	 * Note: If a Component is removed of its Container, then the PopupMenu
	 * is removed as well. After the Component is added again to a Container
	 * the Popupmaenu must added again as well.
	 * This Funktion stores the previous assigned Popupmenu. Use
	 * this Funktion to re-assigin the PopupMenu after a remove/add operation.
	 * @return associtated Popupmenu
	 */
	public PopupMenu getPopUpMenu() {
		return popup;
	}
	
	
	public boolean isVisible() {
		return (lPaint && super.isVisible());
	}
	
	
	
	public void setPaint(boolean lPaint) {
		this.lPaint=lPaint;
		setVisible(lPaint);
	}
	
	
	public boolean getPaint() {
		return(lPaint);
	}
	
	
	
	
	/**
	 * returns preferred Size of this Component
	 * @returns preferred Size of this Component
	 */
	
	public Dimension getPreferredSize() {
		Dimension back=new Dimension(0,0);
		try
		{
			if (lPaint == true) {
				back.height=image.getHeight(this);
				back.width=image.getWidth(this);
			}
		} catch (NullPointerException e) { }
		return back;
	}
	
	/**
	 * returns minumum Size of this Component
	 * @returns minimum Size of this Component
	 */
	
	public Dimension getMinimumSize() {
		return getPreferredSize();
	}
	
	
	public void setMark(boolean lMark) {
	}
	
	
	
	public boolean getMark() {
		return false;
	}
	
	
	public void paint(Graphics g) {
		try
		{
			if (lPaint) {
				g.drawImage(image,0,0,this);
			}
		} catch (NullPointerException e) { }
	}
	
	
	/**
	 * process Mouse Event for this Component.
	 * If a popup Menu is associated with this Component
	 * the Popupmenut is opened with the PopupTrigger.
	 * @param e the MouseEvent for this Component
	 */
	
	public void processMouseEvent(MouseEvent e) {
		if (e.isPopupTrigger()) {
			if (popup != null) {
				popup.show(e.getComponent(), e.getX(), e.getY());
			}
		}
		super.processMouseEvent(e);
	}
	
	
	/**
	 * Set the image, specified with the image name
	 * 
	 * @param name the name of the image which is loaded
	 */
	
	public void setImage(String name) {
		this.filename=name;
		this.image=ImageServer.getImage(name,this);
	}
	
	
	
	
	/**
	 * Returns the String representation of this NodeContainer values.
	 */
	
	public String toString() {
		return getClass().getName() + "[filename="+filename+"]";
		
	}
	
	
	
}

