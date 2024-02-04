// components/Dashboard.js
import React from 'react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
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
        {/* Add more categories as needed */}
      </ul>
    </div>
  );
};

export default Dashboard;
