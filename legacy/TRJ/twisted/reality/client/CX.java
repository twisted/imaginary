package twisted.reality.client;

public abstract class CX
{
	static int version = 0;
	
	transient private CXStub stub;
	transient private int cxnum;
	public final void setStub(CXStub stub, int cxnum)
	{
		this.stub = (CXStub)stub;
		this.cxnum = cxnum;
	}
	
	public void sendData(String s)
	{
		stub.send(cxnum, s);
	}
	
	public void sendData(Object[] message)
	{
		stub.send(cxnum, message);
	}
	
	public void requestStopCX()
	{
		stub.requestStopCX(cxnum);
	}
	public abstract void handleData(Object[] message);
	public abstract void init();
	public abstract void destroy();
}
