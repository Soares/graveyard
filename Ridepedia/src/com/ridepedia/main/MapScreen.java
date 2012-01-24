package com.ridepedia.main;

import javax.microedition.location.Criteria;
import javax.microedition.location.Location;
import javax.microedition.location.LocationProvider;
import javax.microedition.location.QualifiedCoordinates;

import net.rim.device.api.lbs.maps.MapFactory;
import net.rim.device.api.lbs.maps.model.MapPoint;
import net.rim.device.api.lbs.maps.ui.MapAction;
import net.rim.device.api.lbs.maps.ui.RichMapField;
import net.rim.device.api.ui.UiApplication;
import net.rim.device.api.ui.container.FullScreen;

public class MapScreen extends FullScreen {
	
    private Criteria getAssistedCriteria() {
        Criteria criteria = new Criteria();
        criteria.setHorizontalAccuracy(100);
        criteria.setVerticalAccuracy(100);
        criteria.setCostAllowed(true);
        return criteria;
    }
	
	public MapScreen() {
		super(FullScreen.DEFAULT_CLOSE | FullScreen.DEFAULT_MENU);
		Location location = null;
		
		Criteria criteria = getAssistedCriteria();
		try {
			LocationProvider provider = LocationProvider.getInstance(criteria);
			location = provider.getLocation(-1);
		} catch(Exception e) {
			System.out.println(e);
			System.out.println("See, this is why we can't have nice things.");
			UiApplication.getUiApplication().popScreen(this);
			return;
		}
		QualifiedCoordinates coords = location.getQualifiedCoordinates();
		
		RichMapField map = MapFactory.getInstance().generateRichMapField();
		MapAction action = map.getAction();
		MapPoint point = new MapPoint(coords.getLatitude(), coords.getLongitude());
		action.setCentreAndZoom(point, 2);
		add(map);
	}
}
