
/*
  ImageServer loads images
  Copyright (C) 1997  Martin Vogt
  
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation.
  
  for mor information visit fsf.org
  
*/


package twisted.util.swing;

import java.awt.*;
import java.util.*;
import java.io.*;

import java.net.URL;
import java.awt.image.ImageProducer;


/**
 * The Imageserver takes care that you get an Image to a given name.
 * The	Imageserver stores all the names that already have been
 * loaded and a pointer to the already loaded image.
 * If you load the same picture again the Imageserver first
 * looks if this image is already stores and then return
 * the pointer to this image. If the Image on the Harddrive has
 * changed we don´t load the new version, thus there must be a
 * method to force loading from the Harddrive.
 * 
 * The Server must be configured with its searchpath for the icons
 * 
 * @author	   Martin Vogt
 * @version	   0.2, 2 Jun 1997
 */




public class ImageServer {
	
	
	public static String imagePath=".";
	
	static Hashtable loadedImages=new Hashtable();
/*	
	public static void writeCache(String name)
	{
		try
		{
			OutputStream ostream = new FileOutputStream(name);
			ObjectOutputStream p = new ObjectOutputStream(ostream);
			p.writeObject(loadedImages);
		} catch (IOException e) {}
	}
	
	public static void readCache(String name)
	{
		try
		{
			InputStream istream = new FileInputStream(name);
			ObjectInputStream p = new ObjectInputStream(istream);
			loadedImages = (Hashtable)p.readObject();
		} catch (IOException e) {}
		catch (ClassNotFoundException e) {}
	}
*/
	public static URL findResource(String resource, Class clazz)
	{
		// first try to find image in classpath
		URL url;
		url = clazz.getClass().getResource("/" + resource);
		if (url != null)
			return url;
		if (!(resource.endsWith(".gif") || resource.endsWith(".jpg")))
		{
			url = clazz.getClass().getResource("/" + resource + ".gif");
			if (url != null)
				return url;
			url = clazz.getClass().getResource("/" + resource + ".jpg");
			if (url != null)
				return url;
		}
		//if that fails, try to find it in the search path -- later...
		return null;
	}
	
	/**
	 * This return you an Image or null if the image cannot be found
	 * The image is completly loaded befor the Function returns
	 * 
	 * @param path sets the directory path
	 * @param name sets the name of the Image-file
	 * @param comp the Component which control the image download
	 * @returns the Image or null if File Not Found
	 */
	public static Image getImage(String resource,Component where)
	{
		
		try
		{
			Image image;
			URL url = findResource(imagePath + "/" + resource, where.getClass());
			if (url == null)
			{
				System.out.println("Image not found: "+resource);
				return null;
			}
			// look in cache first...
			image=getCacheImage(url.toString());
			if (image != null) {
				return image;
			}
			// next, try to load it...
			image = where.createImage((ImageProducer)url.getContent());
			if (image == null)
				System.out.println("Image isn't an image or something:"+imagePath+"/"+resource);
			else
				insertImage(url.toString(),image);
			return (load(image,where));
		} catch (Exception e) {
			System.out.println("Exception in GetImageResource for "+imagePath+"/"+resource+":" +e);
		}
		return null;
	}
	
/*	Old method....
	public static Image getImage(String name,Component comp)
	{
	File file=new File(iconPath,name);
	return getImage(file,comp);
	}*/
	/**
	 * loads Image from a give file.
	 * @param file the file which is loaded
	 * @param comp the comp which loads the file
	 * @returns the Image or null if File Not Found
	 * 
	 */
/*	  public static Image getImage(File file, Component comp) {
	  Image image;
	  
	  image=getCacheImage(file.getAbsolutePath());
	  if (image != null) {
	  return image;
	  }
	  
	  if (file.exists()) {
	  image=Toolkit.getDefaultToolkit().getImage(file.getPath());
	  insertImage(file.getAbsolutePath(),image);
	  return (load(image,comp));
	  }
	  else {
	  System.out.println("File:"+ file.getAbsolutePath()+" not found!");
	  }
	  return null;
	  }*/
	
	private static int n;
	private static synchronized final int inc ()
	{
		return n++;
	}
	/**
	 * This method completly loads the Image in memory, then returns the
	 * loaded image
	 * 
	 * @param image the image to load
	 * @param comp the Component which control the image download
	 * @returns the fully loaded image
	 */
	public static Image load(Image image, Component comp) {
		MediaTracker tracker;
		int reference=inc();
		tracker	 =	new	 MediaTracker(comp);
		tracker.addImage(image,	 reference);
		try {
			tracker.waitForID(reference);
		}
		catch  (InterruptedException  e) {
			System.err.println("Error tracking image in ImageServer:load");
			System.err.println("exception:"+ e.getMessage());
		}
		return image;
	}
	
	/**
	 * Inserts image in buffer.
	 * @param file the key under which the image is buffered
	 * @param image the value which is buffered
	 */
	static void insertImage(String file, Image image) {
		if (isAlreadyLoaded(file)) {
			deleteFromCache(file);
		}
		loadedImages.put(file,image);
	}
	
	
	/**
	 * Checks if an image is already in the buffer
	 * @param file the key of the image
	 * @return true if image is in buffer
	 */
	static boolean isAlreadyLoaded(String file) {
		return loadedImages.contains(file);
	}
	
	/**
	 * Deletes an image from the buffer
	 * @param file the key for the image which is deleted
	 */
	static void deleteFromCache(String file) {
		if (isAlreadyLoaded(file)) {
			loadedImages.remove(file);
		}
	}
	
	
	/**
	 * returns the image in the buffer
	 * @param file the key for the image
	 * @returns the buffered image
	 */
	static Image getCacheImage(String file) {
		return (Image)loadedImages.get(file);
	}
}

