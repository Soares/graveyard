package com.ridepedia.main;

import net.rim.device.api.ui.Field;
import net.rim.device.api.ui.FieldChangeListener;
import net.rim.device.api.ui.Manager;
import net.rim.device.api.ui.Screen;
import net.rim.device.api.ui.UiApplication;
import net.rim.device.api.ui.component.ButtonField;
import net.rim.device.api.ui.container.MainScreen;

public class WelcomeScreen extends MainScreen {

	public WelcomeScreen() {
		
		/* Button to call a cab */
		ButtonField callCab = new ButtonField("Call a Cab", Field.FIELD_HCENTER);
		callCab.setChangeListener(new FieldChangeListener() {
			public void fieldChanged(Field field, int context) {
				Screen next = new AcceptScreen("Sexy Driver", "http://natesoares.com/media/uploads/sexydriver.jpg", 6);
				UiApplication.getUiApplication().pushScreen(next);
				//Dialog.alert("Searching...");
			}
		});
		callCab.setMargin(Ridepedia.marginTop, 0, 15, 0);
		callCab.setPadding(5, 25, 5, 25);
		
		/* Button to reserve a cab */
		ButtonField reserveCab = new ButtonField("Reserve a Cab", Field.FIELD_HCENTER);
		reserveCab.setEditable(false);
		
		/* Vertical Field Manager */
		Manager manager = new FullVerticalFieldManager(Manager.USE_ALL_WIDTH);
		manager.setBackground(Ridepedia.primary);
		manager.add(callCab);
		manager.add(reserveCab);
		
		/* Screen Settings */
		setBackground(Ridepedia.primary);
		add(manager);
	}
}
