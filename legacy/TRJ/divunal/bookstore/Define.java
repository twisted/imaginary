package divunal.bookstore;

import twisted.reality.*;

public class Define extends Verb
{
	/* hehe.  I'd like to see THIS run on a mac. 
	 * divunal.bookstore.Define$DefineResponseProcessor.class ...
	 *
	 *	FUCK YOU, ever hear of Jar files!!!! ;-)
	 *			-phil, the macintosh avenger
	 */
	public class DefineResponseProcessor implements ResponseProcessor
	{
		public DefineResponseProcessor(String dkey, Thing thin,Player inp,String Kkey)
		{
			mThing=thin;
			mKey=dkey;
			mPlayer=inp;
			mKkey=Kkey;
		}
		public void gotResponse(String s)
		{
			/* enc for "encyclopedia" to save a little memory but
               still avoid namespace conflicts :-) */

			Stack stk = (Stack) mThing.getPersistable("enc index");
			if (stk == null)
			{
				stk=new Stack();
				mThing.putPersistable("enc index",stk);
			}
			if(mThing.getString(mKkey) == null)
				stk.pushString(mKey);
			mThing.putString(mKkey,s);
			mPlayer.hears("Definition set.");
		}
		Thing mThing;
		String mKey;
		String mKkey;
		Player mPlayer;
	}
	
	public Define()
	{
		super("define");
		setDefaultPrep("in");
	}
	
	public boolean action (Sentence d) throws RPException
	{
		Thing book = d.indirectObject("in");
		String word = d.directString();
		String key = "enc define " + word.toLowerCase();
		String definition;
		definition = book.getString(key);
		if (definition==null) definition=word+": ";
		d.subject().hears("You start thinking about the definition of " + d.directString() + "...");
		d.subject().requestResponse
			(
			 new DefineResponseProcessor
			 (
			  word,
			  book,
			  d.subject(),
			  key
			  ),
			 "A definition for " + word,
			 definition
			 );
		return true;
	}
}
