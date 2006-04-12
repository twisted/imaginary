/**
 * A Markov table is a structure used for storing the probabilities
 * of transitioning from an initial state to one of several possible
 * new states.  For example, if you're dealing with weather, your
 * states might be <i>sun, rain,</i> and <i>snow</i>, with your table
 * looking like this:
 *
 *<table cellpadding="5">
 *  <tr><th>Initial States</th></tr>
 *  <tr>
 *    <td>sun</td><td>rain</td><td>snow</td><td>&nbsp;</td><td>&nbsp;</td>
 *  </tr>
 *  <tr>
 *    <td>3</td><td>2</td><td>1</td><td>sun</td><td rowspan="3" valign="center"><b>Possible States</b></td>
 *  </tr>
 *  <tr>
 *    <td>2</td><td>4</td><td>0</td><td>rain</td>
 *  </tr>
 *  <tr>
 *    <td>2</td><td>0</td><td>4</td><td>snow</td>
 *  </tr></table>
 *
 * (If you've studied math, you might be wondering what's up with the
 * table values. Normally, the values in a column are floats whose sum is 1.
 * This class uses ints because it's much easier to implement for the purposes
 * it's likely to be used for.  Bear with us.  :-)
 *
 * By this table, if it's currently sunny, the chance of it starting to rain
 * is 2 in 6, or about 33%.
 *
 * This class also allows you to add an instance of a state, so you can basically
 * log trends.  A different example illustrates this: say you scan a dictionary,
 * sending for each word the sequence of letters to the Markov table.  You could
 * then use the table to generate words that, while not likely to be actual
 * dictionary words, would at least be pronounceable.  This sort of technique 
 * could be used for generating names of places, words in foreign tongues,
 * and good deal many other things.
 *
 * <b>Please note that state names are <i>case-sensitive</i></b>
 *
 * @author Michael Dartt, jedin@twistedmatrix.com
 *
 */


package twisted.util;

/* Possible Improvements
 * ---------------------
 * n-dimensional matrix -- THIS WOULD BE REALLY COOL!!!
 * Resizable/expandable tables (can add states beyond initialization)--ALSO COOL
 * Add comparisons that ignore case
 * Allow forcibly inserting sequences, ignoring nonexsistent states
 * Take sequence length into account
 * Save locations when validating so they don't have to be recalculated
 * Functions: deleteState, swapStates, replaceState, setValuesFrom, setValuesTo
 *
 */

public class MarkovTable
{
    private String[] states;
    //private int max_num_states;
    private int num_states;
    //states[] is used for indexing the probabilities, since a Markov table
    //is square
    private int[][] prob_table;

    //The previous state info has these settings when there's not a sequence active
    private String prev_state = null;
    private int prev_state_loc = -1;

    /**
     * @param states - the table must be created with all of the possible states, each a separate string.
     *
     */
  //Strings are used to make comparisons easier.
    MarkovTable(String[] states)
    {
	this.states = states;
	num_states = states.length; //To save calls later

	prob_table = new int[num_states][num_states];
    }
    
    
    /**
     * Checks to see whether the submitted state exists or not by doing a String
     * comparison that is <i>case-sensitive</i>.
     * @return The position in the array of states if the state exists, -1 otherwise
     *
     */
    public int verifyState(String state)
    {
	int state_loc = 0; //State's location in the array

	while(
	      (state_loc < num_states) &&
	      !(states[state_loc].equals(state))
	      ) 
	{
	    state_loc++;
	}

	if(state_loc == num_states) return -1; //Not in the state array
	else return state_loc;
    }
  
  
  /**
   * Starts a sequence going after verifying the given state--good for 
   * progressively adding occurrences of states.
   * Use this to start a new sequence--no need for an endSequence() function. 
   */
    //Sets the prev_state variables to the given state, if it's legit
    public boolean startSequence(String state)
    {
	int state_loc = verifyState(state);
	
	if (state_loc < 0) return false;  //Not in the array
	else //Found it
	{
       	    prev_state = state;
	    prev_state_loc = state_loc;
	 
	    return true;
	}
    }


  /*
    //Cleans things up
    //You really don't need this--you can just use startSequence again in
    //most cases
    public void endSequence()
    {
    prev_state = null;
    prev_state_loc = -1;
    }*/


  /**
   * Verifies a sequence of states and then adds the entire set of 
   * occurrences to the table.
   */
    //Adds a sequence, first making sure that all of the states are legit
    /* Optimization: save locations from first loop so you don't have to recalc */
    public boolean addSequence(String[] new_states)
    {
	int new_states_len = new_states.length;
	
	//Used for keeping track of where the states are in states[]
	int[] new_states_loc = new int[new_states_len];
	
	int i; //Counting variable!

	//Check all the states.  Exit if any one is not legit
	for (i = 0; i < new_states_len; i++)
	{
	    //Assign returned positions to the location array
	    if ((new_states_loc[i] = verifyState(new_states[i])) < 0) return false;
	}

	//If you're here, everything checked out--go ahead
	startSequence(new_states[0]);

	//Add each state
	for (i = 1; i < new_states_len; i++)
	{
	    addOccurrence(new_states_loc[i]);
	}
	
	return true;
    }

    
  /**
   * Adds the state's occurrence to the current sequence,
   * which must be already started.
   * @param next_state_loc - the location of the state in array of states (can be gotten from verifyState)
   * @return true if the state exits (and performs the add), false otherwise (exits after checking)
   * @see verifyState()
   * @see startSequence()
   */
    //Adds an instance of a state
    public boolean addOccurrence(int next_state_loc)
    {

	//Increment the transition cell for previous state -> next state
	try { prob_table[next_state_loc][prev_state_loc] += 1; }
	
	//If, for whatever reason, there isn't a state there, return false.
	//Likely causes are the location being invalid or the previous state
	//not being set.
	catch (IndexOutOfBoundsException e) { return false; }

	//If you're here, it worked.  The previous state becomes the next state.
	prev_state = states[next_state_loc];
	prev_state_loc = next_state_loc;

	return true;
    }


  /**
   * Verifies the state and adds its occurrence to the current sequence, which 
   * must already be started.
   * @see startSequence()
   */
    //Another way of adding a state that's probably more intuitive for the
    //user.  Useful for progressive adding.
    public boolean addOccurrence(String next_state)
    {
	int new_state_loc = verifyState(next_state);
	
	if (new_state_loc < 0) return false;

	addOccurrence(new_state_loc);
	
	return true;
    }
    

  /**
   * @return The next state from the given one, determined probabalistically; null if the given state isn't valid, i.e. it doesn't exist, or no states can follow it.  (All probabilities are 0.)
   */
    public String getNextState(String state)
    {
	int prob_total = 0; //Sum of all probabilities of potential states
	int state_loc = 0;
	int die_roll; //Random # from 1->prob_total, used for finding next state
	int i; //Ye olde loop variable

	//Find out the state's position in the array
	//If it wasn't in the array, exit
	if ((state_loc = verifyState(state)) < 0) return null;

	//Total up the probabilities
	for (i = 0; i < num_states; i++)
	{
	    prob_total += prob_table[i][state_loc];
	}

	if (prob_total == 0) return null; //nothing can come after this state
	
	//Get a random number to use for finding the next state
	//"1", not "0" is minimum, since states with a 0 shouldn't be chosen
	die_roll = (int)(Math.random() * (prob_total - 1)) + 1;
   
	//Step through the matrix.  Keep a running total again.
	//The next state is the first one where
	//die_roll <= sum(current_state + all_previous_states)
	for (i = 0, prob_total = 0; i < num_states; i++)
	{
	    prob_total += prob_table[i][state_loc];
	    if (die_roll <= prob_total) break;
	}

	return states[i];
    }

    
  /**
   * @return An array of states, generated probabalistically from a randomly-selected start state
   * If a state is chosen from which no other states can follow (probabilities are all 0), the sequence ends there and is returned.
   * @param length - the length of the sequence to be generated
   * @param as_string - if true, returns only one String, which is the concatenation of the returned states, separated by the given separator string, or nothing if null is passed as the separator 
   * @param separator - the String with which to separate each returned state if as_string is set
   */
    //Returns a bunch of states, in their "proper order", starting from 
    //a randomly-chosen one.  
    public String[] getSequence(int length, boolean as_string, String separator)
    {
	String[] seq = new String[length]; //The sequence to return

	//Get the start state
	//I mult. states.length by 2, rather than use a magic number
	//so that you're guaranteed the possibility of a # at least 
	//as big as the length.
	seq[0] = states[(int)(Math.random() * (2 * states.length)) % states.length];

	//If caller wants it as a string, just append to the first state chosen
	if (as_string == true)
	{
	    String str = seq[0];
	    for (int i = 1; i < seq.length; i++)
	    {
		//Remember that str starts with the value of the previous state
		str = getNextState(str); 
		//If null has been returned, no states can follow, so stop
		if (str == null) break;
		else seq[0] += (separator == null ? "" : separator) + str;
	    }
	}
	
	else //Enter states separately
	{
	    for (int i = 1; i < seq.length; i++)
	    {
		seq[i] = getNextState(seq[i-1]);
		//If null has been returned, no states can follow, so stop
		if (seq[i] == null) break;
	    }
	}
	return seq;
    }


  /**
   * Same as previous getSequence, but takes a start state
   * @see getSequence(int length, boolean as_string, String separator)
   */
    public String[] getSequence(String start, int length, boolean as_string, String separator)
    {
	String[] seq = new String[length]; //The sequence to return

	seq[0] = start;

	//If caller wants it as a string, just append to the first state chosen
	if (as_string == true)
	{
	    String str = seq[0];

	    for (int i = 1; i < seq.length; i++)
	    {
		//Remember that str starts with the value of the previous state
		str = getNextState(str); 
		//If null has been returned, no states can follow, so stop
		if (str == null) break;
		else seq[0] += (separator == null ? "" : separator) + str;
	    }
	}
	
	else //Enter states separately
	{
	    for (int i = 1; i < seq.length; i++)
	    {
		seq[i] = getNextState(seq[i-1]);
		//If null has been returned, no states can follow, so stop
		if (seq[i] == null) break;
	    }
	}
	return seq;
    }
	

  /**
   * Prints the table to stdout, with some nice (naive) formatting to get
   * readable rows and columns (like the opening example in ASCII)
   */
    public void printTable()
    {
	int i;
	String table_row = "";

	//Print the states as column headers
	for (i = 0; i < num_states; i++)
	    table_row += states[i] + "\t";
	System.out.println(table_row);

	//Print the rows of values, with corresponding states following
	for (i = 0; i < num_states; i++)
	{
	    //Reinitialize table_row
	    table_row = "";
	    
	    //Get a string of the values
	    for (int j = 0; j < num_states; j++)
	    {
		table_row += prob_table[i][j] + "\t"; 
	    }
	    
	    //Print the row with the state label and a newline
	    System.out.println(table_row + states[i]);
	}
    }
}
	    
