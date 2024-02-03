import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import CategoryScores from './components/CategoryScores';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/categories/:categoryId" element={<CategoryScores />} />
      </Routes>
    </Router>
  );
}

export default App;
