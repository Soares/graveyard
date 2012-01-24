package com.ridepedia.main;

import net.rim.device.api.ui.Field;
import net.rim.device.api.ui.FieldChangeListener;
import net.rim.device.api.ui.Manager;
import net.rim.device.api.ui.Screen;
import net.rim.device.api.ui.UiApplication;
import net.rim.device.api.ui.component.ButtonField;
import net.rim.device.api.ui.component.LabelField;
import net.rim.device.api.ui.container.FullScreen;

public class AcceptScreen extends FullScreen {
	public AcceptScreen(String name, String url, int minutes) {
		Field label = new LabelField(name, Field.FIELD_HCENTER);
		label.setMargin(Ridepedia.marginTop, 0, 15, 0);
		
		Field image = new WebImageField(url, Field.FIELD_HCENTER);
		
		Field eta = new LabelField("ETA: " + minutes + " minutes.", Field.FIELD_HCENTER);
		eta.setMargin(20, 0, 20, 0);
		
		Field accept = new ButtonField("Accept", Field.FIELD_HCENTER);
		accept.setChangeListener(new FieldChangeListener() {
			public void fieldChanged(Field field, int context) {
				Screen next = new MapScreen();
				UiApplication app = UiApplication.getUiApplication();
				app.popScreen(app.getActiveScreen());
				app.pushScreen(next);
			}
		});
		accept.setPadding(5, 25, 5, 25);
		accept.setMargin(60, 0, 20, 0);
		
		Field cancel = new ButtonField("Cancel", Field.FIELD_RIGHT);
		cancel.setChangeListener(new FieldChangeListener() {
			public void fieldChanged(Field field, int context) {
				UiApplication app = UiApplication.getUiApplication();
				app.popScreen(app.getActiveScreen());
			}
		});
			
		Manager manager = new FullVerticalFieldManager(Manager.USE_ALL_WIDTH);
		manager.setBackground(Ridepedia.primary);
		manager.add(label);
		manager.add(image);
		manager.add(eta);
		
		manager.add(accept);
		manager.add(cancel);
		
		add(manager);
	}
}
