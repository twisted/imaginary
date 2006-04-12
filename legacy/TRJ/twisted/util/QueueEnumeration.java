package twisted.util;

import java.util.Enumeration;

public class QueueEnumeration implements Enumeration
{
	class QueueLink
	{
		public QueueLink(Object inVal)
		{
			val=inVal;
		}
		QueueLink next;
		Object val;
	}
	
	QueueLink q;
	QueueLink start;
	
	int elementCount;
	
	/**
	 * Add an element to the queue, if the element is non-null.
	 * Nulls are ignored.
	 */
	
	public synchronized void enQueue(Object o)
	{
		if (o!=null)
		{
			if (q!=null)
			{
				q.next=new QueueLink(o);
				q=q.next;
			}
			else
			{
				q=start=new QueueLink(o);
			}
			elementCount++;
		}
	}
	
	/**
	 * Returns the number of elements remaining in the queue.
	 */
	
	public int size()
	{
		return elementCount;
	}
	public synchronized Object nextElement()
	{
		if (start != null)
		{
			QueueLink nq = start;
			start=start.next;
			if (nq==q)
			{
				if (start != null)
					System.out.println
						("twisted.util.QueueEnumeration is broken.");
				q=null;
			}
			
			elementCount--;
			return nq.val;
		}
		else return null;
	}
	
	public boolean hasMoreElements()
	{
		return start!=null;
	}
}
