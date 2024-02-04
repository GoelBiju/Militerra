// components/Dashboard.js
import { Link } from "react-router-dom";
import "leaflet/dist/leaflet.css";
import GeocodeSearch from "./GeocodeSearch"; // Your existing search component
import MapComponent from "../components/mapComponent"; // The map component you just created
import React, { useState } from "react";

const Dashboard = () => {
  const [position, setPosition] = useState([51.505, -0.09]); // Default position
  const handleSearchResult = (newPosition) => {
    setPosition(newPosition);
  };

  return (
    <div>
      <h1>Fitness Dashboard</h1>
      <ul>
        <li>
          <Link to="/categories/physical">Physical Fitness</Link>
        </li>
        <li>
          <Link to="/categories/endurance">Endurance</Link>
        </li>
      </ul>
      <div className="App">
        <GeocodeSearch onResult={handleSearchResult} />
        <MapComponent position={position} />
      </div>
    </div>
  );
};

export default Dashboard;
