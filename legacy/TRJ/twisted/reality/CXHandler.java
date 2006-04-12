package twisted.reality;

/**
 * This is a handler class for client-side user-interface extensions.
 * This feature is far from complete, but it's in here so people can
 * hack on it.  (Translation: don't use it in an actual game.  We're
 * not using it in ours yet.)
 * 
 * @version 1.0.0, 12 Jun 1999
 * @author James Knight
 */

abstract class CXHandler
{
	protected Object cid;
	protected RealityUI ui;
	
	/**
	 * Called from the RealityUI whenever there is data from the remote client
	 * 
	 * @param	message an array of data (String or byte[] recieved from the client 
	 */
	protected abstract void handleData(Object[] message);
	
	/**
	 * Determines what the name of the class to handle data on the remote end is.
	 * 
	 * @return	a string containing the name of the class that will handle
	 * the data on the client end.
	 */
	public abstract String getClientClass();
	
	/**
	 * Performs all initialization necessary to startup the client extension.
	 * 
	 * If you override it, It *MUST* call super.init(ui, cid);
	 * 
	 * @param	ui	the RealityUI attached the client running the CX.
	 * @param	cid	the connection reference ID number, indicating which connection
	 * 				you are talking through
	 */
	protected void init(Object ui, Object cid)
	{
		this.ui=(RealityUI)ui;
		this.cid=cid;
	}
	
	/**
	 * Called when the client requests to close the extension.
	 *
	 * To actually close the connection, call stopCX(). If you do not
	 * call that function, the close request will be ignored and the connection
	 * will stay open.
	 */
	protected abstract void handleClose();
	
	/**
	 * Called right before the connection is actually closed. Final cleanup should be
	 * done here. No more communication is possible at this point.
	 */
	protected abstract void destroy();
	
	/**
	 * Sends the specified message to the remote client extension
	 */
	protected final void sendCXData(String message)
	{
		ui.sendCXData(cid, message);
	}
	
	/**
	 * Sends the specified message to the remote client extension
	 */
	protected final void sendCXData(Object[] message)
	{
		ui.sendCXData(cid, message);
	}
	
	/**
	 * Tells the remote client extension to close and shuts down the connection.
	 */
	public final void stopCX()
	{
		ui.stopCX(cid);
	}
}
