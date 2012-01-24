package com.ridepedia.main;

import net.rim.device.api.ui.UiApplication;
import net.rim.device.api.ui.decor.Background;
import net.rim.device.api.ui.decor.BackgroundFactory;

public class Ridepedia extends UiApplication {
	/* Styles (0x00D4A017 is a good yellow) */
	public static final Background primary = BackgroundFactory.createSolidBackground(0x00D4A017);
	public static final int marginTop = 60;
	
	public Ridepedia() {
		super();
		WelcomeScreen screen = new WelcomeScreen();
		pushScreen(screen);
	}
	
	public static void main(String[] args) {
		new Ridepedia().enterEventDispatcher();
	}
}