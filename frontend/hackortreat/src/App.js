// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ResultsPage from './pages/ResultsPage';
import ComparePage from './pages/ComparePage';
import LeaderboardPage from './pages/LeaderboardPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navigation */}
        <nav className="navbar">
          <div className="nav-brand">
            <h1>🎴 Card Analyzer</h1>
          </div>
          <div className="nav-links">
            <Link to="/">Upload</Link>
            <Link to="/compare">Compare</Link>
            <Link to="/leaderboard">Wall of Fame</Link>
          </div>
        </nav>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="/compare" element={<ComparePage />} />
          <Route path="/leaderboard" element={<LeaderboardPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
