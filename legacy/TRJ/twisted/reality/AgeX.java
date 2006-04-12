package twisted.reality;

class AgeX implements Runnable
{
	Age x;
	AgeX(Age X)
	{
		x=X;
	}
	public void run()
	{
		int CurrentFileStatus = 0;
		while(true)
		{
			for(int i = 0;i<400;i++)
			{
				try { Thread.sleep(2712); } catch (InterruptedException e) {  }
				x.doEventStuff();
			}
			
			// this autosave stuff gets pretty hairy.  you can run
			// into a bunch of places where data just doesn't get
			// saved.  Try to avoid this.

			/*
			  synchronized(x)
			  {
			  CurrentFileStatus++;
			  CurrentFileStatus = CurrentFileStatus % 3;
			  Age.log("Writing File..."+CurrentFileStatus+'@'+new Date());
			  x.PersisttoFile("autosave." + CurrentFileStatus);
			  Age.log("Finished File..."+CurrentFileStatus+'@'+new Date());
			  }
			*/
		}
	}
}

