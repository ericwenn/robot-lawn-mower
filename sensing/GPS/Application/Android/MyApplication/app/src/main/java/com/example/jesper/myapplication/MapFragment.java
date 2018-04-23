package com.example.jesper.myapplication;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapView;
import com.google.android.gms.maps.MapsInitializer;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.CameraPosition;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

/**
 * Created by jesper on 2018-04-18.
 */

public class MapFragment extends Fragment implements OnMapReadyCallback {
    GoogleMap googleMap;
    MapView mapView;
    View view;

    public MapFragment(){

    }

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState){
        this.view = inflater.inflate(R.layout.map_fragment, container, false);
        return this.view;

    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState){
        super.onViewCreated(view, savedInstanceState);

        this.mapView = (MapView) this.view.findViewById(R.id.map);
        if(this.mapView != null){
            this.mapView.onCreate(null);
            this.mapView.onResume();
            this.mapView.getMapAsync(this);

        }
    }

    @Override
    public void onMapReady(GoogleMap googleMap){
        MapsInitializer.initialize(getContext());

        this.googleMap = googleMap;
        googleMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);
        googleMap.addMarker(new MarkerOptions().position(new LatLng(57,11)));
        CameraPosition location = CameraPosition.builder().target(new LatLng(57,11)).build();
        googleMap.moveCamera(CameraUpdateFactory.newCameraPosition(location));
    }
}
