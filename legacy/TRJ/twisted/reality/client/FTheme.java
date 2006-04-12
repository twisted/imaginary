package twisted.reality.client;
import javax.swing.plaf.metal.DefaultMetalTheme;
import javax.swing.plaf.ColorUIResource;
import java.awt.Color;
import javax.swing.UIDefaults;
public class FTheme extends DefaultMetalTheme
{
	// default constructor
	FTheme()
	{
		black=Color.black;
		white=Color.white;
		primary1=new Color(102, 102, 102);
		primary2=new Color(153, 153, 153);
		primary3=new Color(204, 204, 204);
		secondary1=new Color(102, 102, 102);
		secondary2=new Color(153, 153, 153);
		secondary3=new Color(204, 204, 204);
	}

	FTheme(Color wh, Color bk, Color p1, Color p2, Color p3, Color s1, Color s2, Color s3)
	{
		black=bk;
		white=wh;
		primary1=p1;
		primary2=p2;
		primary3=p3;
		secondary1=s1;
		secondary2=s2;
		secondary3=s3;
	}

	ColorUIResource mcr(Color a)
	{
		return new ColorUIResource(a);
	}

	private Color primary1;
	private Color primary2;
	private Color primary3;

	private Color secondary1;
	private Color secondary2;
	private Color secondary3;

	private Color black;
	private Color white;

	public ColorUIResource getPrimary1() { return mcr(primary1); }
	public ColorUIResource getPrimary2() { return mcr(primary2); }
	public ColorUIResource getPrimary3() { return mcr(primary3); }

	public ColorUIResource getSecondary1() { return mcr(secondary1); }
	public ColorUIResource getSecondary2() { return mcr(secondary2); }
	public ColorUIResource getSecondary3() { return mcr(secondary3); }

	public ColorUIResource getBlack() { return mcr(black); }
	public ColorUIResource getWhite() { return mcr(white); }

	public void addCustomEntriesToTable(UIDefaults table)
	{
		table.put("SplitPane.dividerSize", new Integer(4));
		table.put("Tree.leftChildIndent", new Integer(3));
	    table.put("Tree.rightChildIndent", new Integer(7));
	}
}
