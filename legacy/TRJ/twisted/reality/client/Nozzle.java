package twisted.reality.client;

import java.util.Vector;

public interface Nozzle
{
	void handleError(Throwable t);
	void requestResponse(String ID, String prompt, String deftext);
	void setTheme(String theme);
	void hears(String string);
	void setName(Vector name);
	void setExits(Vector exits);
	void completeAction();
	void dialog(String text);
	void setDescription(String desc);
	void logout();

	void addItem(String item, String container, String desc);
	void removeItem(String item, String container);
	void enterItem(String item, String container, String desc);
	void leaveItem(String item, String container, String desc);
	void clearItems();
}
