package com.ridepedia.main;

import net.rim.device.api.ui.component.BitmapField;

public class WebImageField extends BitmapField {
	public WebImageField(String url) {
		this(url, 0);
	}
	
	public WebImageField(String url, long style) {
		super(WebRunner.downloadImage(url), style);
	}
}
