import React, { useState, useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMapEvents,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";

import MediaCard from "./MediaCard";
// Define your custom icon
const soldierIcon = new L.Icon({
  iconUrl: "/soldier-removebg-preview.png",
  iconSize: [38, 95], // Adjust based on your icon's size
  shadowSize: [50, 64], // Adjust based on your shadow image's size, omit if not applicable
  iconAnchor: [22, 94], // Adjust so the tip of the icon points to the exact location
  shadowAnchor: [4, 62], // Adjust, omit if not applicable
  popupAnchor: [-3, -76], // Adjust if you use popups
});

function DraggableMarker(positionData) {
  // Set the initial position to the soldier's current location
  const [position, setPosition] = useState(positionData); // Example coordinates

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
      <Popup>TERRA API INFORMATION</Popup>
    </Marker>
  );
}

function MapComponent({ soldiersData }) {
  return (
    <MapContainer
      center={[51.8833, -3.4333]}
      zoom={13}
      style={{ height: "600px", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {/* Object.entries(a).map(([key, value]) => <DraggableMarker positionData={value[""]} />) */}
    </MapContainer>
  );
}

// Usage of MapComponent, providing the initial position as props
export default function App() {
  // Initialize soldiersData as an object
  const [soldiersData, setSoldiersData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSoldiers = async () => {
      setIsLoading(true);
      try {
        // Use Axios to make the request
        const response = await axios.get("http://127.0.0.1:8000/soldiers");
        setSoldiersData(response.data); // Axios wraps the response data inside the `data` property
      } catch (error) {
        // Axios error handling
        setError(error.response ? error.response.data.message : error.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSoldiers();
  }, []);

  return (
    <div style={{ display: "block", textAlign: "center" }}>
      <div style={{ padding: "20px 35px" }}>
        <MapComponent initialPosition={soldiersData} />
      </div>
      <div>
        <h1 style={{ fontSize: "40px" }}>Soldier Information</h1>
      </div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
          padding: "100px 100px",
          gap: "20px",
        }}
      >
        {isLoading ? (
          <p>Loading...</p>
        ) : error ? (
          <p>Error: {error}</p>
        ) : (
          Object.entries(soldiersData).map(([key, soldierData], idx) => (
            <div key={key} style={{ display: "inline-block" }}>
              <MediaCard data={soldierData} />
            </div>
          ))
        )}
      </div>
    </div>
  );
}
