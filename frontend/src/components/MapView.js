import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function MapView() {
  return (
    <MapContainer
      center={[40.7128, -74.0060]} // NYC coords
      zoom={15}
      style={{ height: '100vh', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[40.7128, -74.0060]}>
        <Popup>You're here.</Popup>
      </Marker>
    </MapContainer>
  );
}

export default MapView;
  