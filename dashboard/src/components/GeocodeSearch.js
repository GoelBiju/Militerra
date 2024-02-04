import React, { useState } from "react";
import axios from "axios";

function GeocodeSearch({ onResult }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const handleSearch = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/geocode", {
        params: { q: query },
      });
      const data = response.data;
      if (data && data.length > 0) {
        const { lat, lon } = data[0]; // Assuming the API returns an array and we take the first result
        onResult([parseFloat(lat), parseFloat(lon)]); // Call the prop function with the lat, lon
      }
    } catch (error) {
      console.error("Error fetching geocode data:", error);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for a location"
      />
      <button onClick={handleSearch}>Search</button>
      <div>
        {results.map((result, index) => (
          <div key={index}>
            <div>
              <strong>Address:</strong> {result.display_name}
            </div>
            <div>
              <strong>Coordinates:</strong> {result.lat}, {result.lon}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default GeocodeSearch;
