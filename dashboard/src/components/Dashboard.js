// components/Dashboard.js
import { Link } from "react-router-dom";
import "leaflet/dist/leaflet.css";
import GeocodeSearch from "./GeocodeSearch"; // Your existing search component
import MapComponent from "../components/mapComponent"; // The map component you just created
import React, { useState } from "react";

const Dashboard = () => {
  // const [position, setPosition] = useState([51.505, -0.09]); // Default position
  // const handleSearchResult = (newPosition) => {
  //   setPosition(newPosition);
  // };

  return (
    <div>
      <h1
        style={{
          textAlign: "center",
          fontFamily: "Helvatica",
          color: "red",
        }}
      >
        MISSION IN PROGRESS
      </h1>
      {/* <ul
        style={{
          listStyle: "none",
          display: "flex",
          float: "right",
          margin: "20px",
          fontSize: "20px",
          fontWeight: "Bold",
        }}
      >
        <li
          style={{
            borderBottom: "2px solid red",
            borderLeft: "2px solid red",
            borderRadius: "10px",
            margin: "20px",
            padding: "10px",
          }}
        >
          <Link
            to="/categories/physical"
            style={{ textDecoration: "none", color: "Green" }}
          >
            Physical Fitness
          </Link>
        </li>
        <li
          style={{
            borderBottom: "2px solid red",
            borderLeft: "2px solid red",
            borderRadius: "10px",
            margin: "20px",
            padding: "10px",
          }}
        >
          <Link
            to="/categories/endurance"
            style={{ textDecoration: "none", color: "Green" }}
          >
            Endurance
          </Link>
        </li>
      </ul> */}

      <div className="App">
        {/* <GeocodeSearch onResult={handleSearchResult} /> */}
        <MapComponent />
      </div>
    </div>
  );
};

export default Dashboard;
