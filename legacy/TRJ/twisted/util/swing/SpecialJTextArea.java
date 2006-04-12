package twisted.util.swing;
import javax.swing.JTextArea;
import javax.swing.text.Document;
/**
 * Massive amounts of hackage...
 * Basically a JTextArea, but forced to be clear and with 4 char tabs,
 * since swing doesn't believe the app when it changes settings like that
 * in a normal way.
 */
 
class SpecialJTextArea extends JTextArea
{
	public SpecialJTextArea() { super(); }
	public SpecialJTextArea(String text) { super(text); }
	public SpecialJTextArea(Document doc) { super(doc); }
	public SpecialJTextArea(Document doc, String text, int rows, int columns) { super(doc,text,rows,columns); }
	public SpecialJTextArea(int rows, int columns) { super(rows,columns); }
	public SpecialJTextArea(String text, int rows, int columns) { super(text,rows,columns); }
	
	public int getTabSize()
	{
		return 4;
	}
	public void setOpaque(boolean b)
	{
		super.setOpaque(false);
	}
}
