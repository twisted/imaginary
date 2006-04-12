package twisted.util.parse;


public class ParseException extends Exception
{
	// build your own exception -- put in line numbers and error
	// detection data, whatever

	// Perhaps you could also build some other errortypes off of
	// this... like class MissingSemiException extends ParseException
	// to delineate a missing semicolon...
	//
	// then throw them using "throw new MissingSemiException();"
}
