package twisted.reality.client;

class CXStub
{
	private Faucet faucet;
	
	protected CXStub(Faucet faucet)
	{
		this.faucet = faucet;
	}

	public void send(int cxnum, String message)
	{
		String[] m = {String.valueOf(cxnum), message};
		faucet.send(Faucet.CMD_CXData, m);
	}
	public void send(int cxnum, Object[] message)
	{
		Object[] m = new Object[message.length+1];
		System.arraycopy(message, 0, m, 1, message.length);
		m[0] = String.valueOf(cxnum);
		faucet.send(Faucet.CMD_CXData, message);
	}
	public void requestStopCX(int cxnum)
	{
		faucet.send(Faucet.CMD_CXRequestStop, String.valueOf(cxnum));
	}
}
