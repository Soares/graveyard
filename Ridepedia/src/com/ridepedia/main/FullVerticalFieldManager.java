package com.ridepedia.main;

import net.rim.device.api.system.Display;
import net.rim.device.api.ui.container.VerticalFieldManager;

public class FullVerticalFieldManager extends VerticalFieldManager {
	public FullVerticalFieldManager() {
		super();
	}
	
    public FullVerticalFieldManager(long flags) {
		super(flags);
	}

	protected void sublayout( int maxWidth, int maxHeight )
    {
        int width = Display.getWidth();
        int height = Display.getHeight();

        super.sublayout(width, height);
        setExtent(width, height);
    }
}
