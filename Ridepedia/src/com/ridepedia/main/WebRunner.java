package com.ridepedia.main;

import java.io.IOException;
import java.io.InputStream;

import javax.microedition.io.Connector;
import javax.microedition.io.HttpConnection;

import net.rim.device.api.io.IOUtilities;
import net.rim.device.api.system.Bitmap;
import net.rim.device.api.system.EncodedImage;

public class WebRunner {
	public static InputStream download(String url) throws IOException {
		HttpConnection connection = null;

		try {
			connection = (HttpConnection)Connector.open(url);
			int responseCode = connection.getResponseCode();
			if(responseCode != HttpConnection.HTTP_OK) {
				throw new IOException("HTTP response code: " + responseCode);
			}
			return connection.openInputStream();
		} finally {
			if(connection != null) connection.close();
		}
	}
	
	public static Bitmap decodeImage(InputStream stream) throws IOException {
		byte[] bytes = IOUtilities.streamToBytes(stream);
		stream.close();
		EncodedImage image = EncodedImage.createEncodedImage(bytes, 0, bytes.length);
		return image.getBitmap();
	}
	
	public static Bitmap downloadImage(String url) {
		try {
			return decodeImage(download(url));
		} catch(IOException e) {
			System.out.println("Returning broken image icon");
			return null;
		}
	}
}
