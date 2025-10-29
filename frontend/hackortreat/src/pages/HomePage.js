import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';
import batemanEyes from '../assets/bateman-eyes.jpg';

export default function HomePage() {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const navigate = useNavigate();

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleAnalyze = () => {
    if (selectedFile) {
      setIsAnalyzing(true);
      // Show analyzing modal for 3 seconds, then navigate to results
      setTimeout(() => {
        setIsAnalyzing(false);
        navigate('/results');
      }, 3000);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">
              <div className="logo-icon-inner"></div>
            </div>
            <h1 className="logo-text">PIERCE & PIERCE</h1>
          </div>
          <nav className="nav">
            <a href="#" className="nav-link">HOME</a>
            <a href="#" className="nav-link">HISTORY</a>
            <a href="#" className="nav-link">CONTACT</a>
            <button className="user-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="title-section">
          <h2 className="main-title">Business Card Analysis</h2>
          <p className="subtitle">
            Is it the subtle off-white coloring? The tasteful thickness? Or perhaps... the watermark? Let's stop guessing. 
            Use this Analyzer to determine your card's true, unassailable superiority. 
          </p>
        </div>

        {/* Upload Area */}
        <div
          className={`upload-area ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
          </svg>
          <h3 className="upload-title">Drag & Drop Your Card Here...If You Dare.</h3>
          <p className="upload-subtitle">or, if you must, click to browse</p>
          
          <label htmlFor="file-upload">
            <input
              id="file-upload"
              type="file"
              className="file-input"
              accept="image/*"
              onChange={handleFileSelect}
            />
            <span className="select-file-btn">SELECT FILE</span>
          </label>
          
          {selectedFile && (
            <p className="selected-file">
              Selected: <strong>{selectedFile.name}</strong>
            </p>
          )}
        </div>

        {/* Analyze Button */}
        <div className="analyze-btn-container">
          <button
            onClick={handleAnalyze}
            disabled={!selectedFile}
            className="analyze-btn"
          >
            ANALYZE CARD
          </button>
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-links">
            <a href="#" className="footer-link">About Us</a>
            <a href="#" className="footer-link">Privacy Policy</a>
            <a href="#" className="footer-link">Terms of Service</a>
          </div>
          <p className="copyright">© 2024 Pierce & Pierce. All Rights Reserved.</p>
        </div>
      </footer>

      {/* Analyzing Modal */}
      {isAnalyzing && (
        <div className="modal-overlay">
          <div className="modal-content">
            <img 
              src={batemanEyes} 
              alt="Analyzing" 
              className="bateman-image"
            />
            <p className="analyzing-text">ANALYZING NOW...</p>
          </div>
        </div>
      )}
    </div>
  );
}