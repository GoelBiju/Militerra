// src/App.js
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './App.css';

function App() {
  const position = [51.505, -0.09]; // Latitude and Longitude for the marker

  return (
    <div className="App">
      <MapContainer
        center={position}
        zoom={13}
        style={{ height: '500px', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        <Marker position={position}>
          <Popup>
            A marker at this location! <br /> (You can customize this popup content.)
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}

export default App;
