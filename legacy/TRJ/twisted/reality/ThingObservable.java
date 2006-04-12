package twisted.reality;

import java.util.Observable;

/**
 * This class is used for watching changes to Things that Players care
 * about (for things like automatic focus changes).
 */

class ThingObservable extends Observable
{
	public synchronized void notifyObservers(Object arg)
	{
		setChanged();
		super.notifyObservers(arg);
	}
}
