package divunal.tenth;

import java.util.Vector;
import twisted.reality.*;
import divunal.tenth.TieUntie;

public class WearRemoveTie extends Verb
{
	static ClothingSlots mySlots=new ClothingSlots();

	
	public static java.util.Enumeration getAllSlots()
	{
		return mySlots.another();
	}
	
	static class ClothingSlots implements java.util.Enumeration
	{
		ClothingSlot next;

		ClothingSlots(ClothingSlot begin)
		{
			next=begin;
		}
		ClothingSlots()
		{
			add("crown");
			add("left eye");
			add("right eye");
			add("left ear");
			add("right ear");
			
			add("neck");
			add("chest");
			
			add("left arm");
			add("right arm");
			add("left wrist");
			add("right wrist");
			add("left hand");
			add("right hand");
			add("left fingers");
			add("right fingers");
			
			add("waist");
			add("left leg");
			add("right leg");
			add("left ankle");
			add("right ankle");
			add("left foot");
			add("right foot");
		}
		
		ClothingSlots another()
		{
			return new ClothingSlots(next);
		}
		
		private void add(String str)
		{
			next=new ClothingSlot(str,next);
		}
		
		public boolean hasMoreElements()
		{
			return (next != null);
		}
		
		public Object nextElement()
		{
			if (next==null) return null;
			String ret = next.string;
			next=next.next;
			return ret;
		}
		
		class ClothingSlot
		{
			String string;
			ClothingSlot next;
			ClothingSlot(String name,ClothingSlot slot)
			{
				string=name;
				next=slot;
			}
		}
	}
	
	public WearRemoveTie()
	{
		super("wear");
		alias("remove");
	}
	
	/*
	  Properties: "clothing worn" -- is this object a currently worn
	  piece of clothing?

	  "clothing "+X -- (where X is the name of a location on your
	  body, as listed above) what is being worn on this area of a
	  player's body?
	  
	  "clothing location" or "clothing location "+N where N is a
	  number (2 or greater) What locations is this clothing worn on?
	*/

	public boolean action(Sentence d) throws RPException
	{
		Thing cloth = d.directObject();
		if (cloth != d.verbObject())
		{
			return false;
		}
		java.util.Enumeration jue = getAllSlots();
		
		String wearon ="clothing location";
		String wearwhere;
		int counter=2;
		twisted.util.LinkedList ll=new twisted.util.LinkedList();
		
		if (cloth.place()!=d.subject())
		{
			d.subject().hears("You don't have that.");
			return true;
		}
		
		while( (wearwhere = cloth.getString(wearon)) != null )
		{
			ll.addElement(wearwhere);
			wearon = "clothing location " + (counter++);
		}
		
		if (d.verbString().equals("wear"))
		{
			if (cloth.getBool("clothing worn"))
			{
				d.subject().hears("You're already wearing that!");
			}
			else
			{
				java.util.Enumeration mye = ll.elements();
				if(mye.hasMoreElements())
				{
					while(mye.hasMoreElements())
					{
						String mys = "clothing "+mye.nextElement();
						Persistable myp = d.subject().getPersistable(mys);
						if (myp==null)
						{
							myp=new Stack();
							d.subject().putPersistable(mys,myp);
						}
						Stack s = (Stack) myp;
						s.pushThing(cloth);
					}
					cloth.putBool("clothing worn",true);
					cloth.setComponent(true);
					if (cloth.getBool("tied") == true)
						divunal.tenth.TieUntie.untie(cloth);
					Object[] cw = {cloth, ": worn."};
					d.subject().hears(cw);
					descript(d.subject());
				}
				else		
					d.subject().hears("That's unwearable -- it wouldn't cover anything.");
			}
		}
		else /* if (d.verbString().equals("remove")) */
		{
			if (!cloth.getBool("clothing worn"))
			{
				d.subject().hears("You're not wearing that!");
			}
			else
			{
				java.util.Enumeration e = ll.elements();
				java.util.Enumeration e2;
				twisted.util.LinkedList stacks = new twisted.util.LinkedList();
				int i=0;
				while (e.hasMoreElements())
				{
					String mys = "clothing "+e.nextElement();
					Stack stk = ((Stack) d.subject().getPersistable(mys));
					if (stk != null)
					{
						Thing clothA = stk.peekThing();
						/*dict.put(clothA,clothA.getString("clothing appearance"));*/
						if (clothA!=cloth)
						{
							d.subject().hears("You'd have to remove some other layers first.");
							return true;
						}
						stacks.put(mys,stk);
					}
					else
					{
						d.subject().hears("Woah.  You should *never* hear this.  Advise an Archetype of the following: problem in divunal.common.clothes.WearRemove");
						return true;
					}
				}
				e=stacks.elements();
				e2=stacks.keys();
				while(e.hasMoreElements())
				{
					Stack stk2 = (Stack)e.nextElement();
					String stkey = (String) e2.nextElement();
					stk2.popThing();
					/* shouldn't this be "hasPop"? */
					if (!stk2.elements().hasMoreElements())
						d.subject().removeProp(stkey);
					/* remove the clothes from the top of each stack */
				}
				cloth.putBool("clothing worn",false);
				cloth.setComponent(false);
				descript(d.subject());
				divunal.tenth.TieUntie.untie(cloth);				
				Object[] cr = {cloth,": removed."};
				d.subject().hears(cr);
			}
		}
		return true;
	}
	
	public static void descript(Thing t)
	{
		java.util.Enumeration e = getAllSlots();
		java.util.Dictionary dict = new twisted.util.LinkedList();
		
		while (e.hasMoreElements())
		{
			Stack stk = ((Stack) t.getPersistable("clothing "+e.nextElement()));
			if (stk != null)
			{
				Thing clothA = stk.peekThing();
				if (clothA != null)
				{
					String clothDescriptor=clothA.getString("clothing appearance");
					Object[] clothapp=clothA.getObjects("clothing appearance");
					
					if (clothapp ==null)
					{
						clothapp = new Object[1];
						clothapp[0]=clothA.getString("clothing appearance");
					}
					
					if (clothapp[0] == null)
					{
						//clothDescriptor = clothA.aan() + clothA.name();
						clothapp[0]=clothA;
					}
					
					dict.put(clothA,clothapp);
				}
			}
		}
		
		e=dict.elements();
		Vector vct = new Vector();
		if (e.hasMoreElements())
		{
			vct.addElement(Pronoun.Of(t));
			vct.addElement(" is wearing ");
			while (e.hasMoreElements())
			{
				Object[] s = (Object[]) e.nextElement();
				
				if (!e.hasMoreElements())
				{
					if (dict.size() > 1)
					{
						vct.addElement("and ");
					}
				}
				for (int i = 0; i < s.length; i++)
				{
					vct.addElement(s[i]);
				}
				
				if (e.hasMoreElements())
				{
					vct.addElement(", ");
				}
				else
				{
					vct.addElement(".");
				}
			}
			
			t.putDescriptor("clothing",vct);
		}
		else
		{
			t.removeDescriptor("clothing");
		}
	}
}
