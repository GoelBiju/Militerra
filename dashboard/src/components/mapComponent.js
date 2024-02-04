import React, { useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMapEvents,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Define your custom icon
const soldierIcon = new L.Icon({
  iconUrl: "/soldier.jpeg",
  iconSize: [38, 95], // Adjust based on your icon's size
  shadowSize: [50, 64], // Adjust based on your shadow image's size, omit if not applicable
  iconAnchor: [22, 94], // Adjust so the tip of the icon points to the exact location
  shadowAnchor: [4, 62], // Adjust, omit if not applicable
  popupAnchor: [-3, -76], // Adjust if you use popups
});

function DraggableMarker() {
  // Set the initial position to the soldier's current location
  const [position, setPosition] = useState([51.505, -0.09]); // Example coordinates

  useMapEvents({
    click(e) {
      setPosition(e.latlng);
    },
  });

  const markerRef = React.useRef(null);
  const eventHandlers = React.useMemo(
    () => ({
      dragend() {
        const marker = markerRef.current;
        if (marker != null) {
          setPosition(marker.getLatLng());
        }
      },
    }),
    []
  );

  return (
    <Marker
      draggable={true}
      eventHandlers={eventHandlers}
      position={position}
      ref={markerRef}
      icon={soldierIcon}
    >
      <Popup>You can move me</Popup>
    </Marker>
  );
}

function MapComponent({ initialPosition }) {
  return (
    <MapContainer
      center={initialPosition}
      zoom={13}
      style={{ height: "400px", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      <DraggableMarker />
    </MapContainer>
  );
}

// Usage of MapComponent, providing the initial position as props
export default function App() {
  // Soldier's current location as the initial position
  const soldierCurrentLocation = [51.505, -0.09]; // Replace with actual coordinates

  return <MapComponent initialPosition={soldierCurrentLocation} />;
}
