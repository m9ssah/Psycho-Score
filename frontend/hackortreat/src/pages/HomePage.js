import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';
import batemanEyes from '../assets/bateman-eyes.jpg';

// TODO: replace with real input
const analysisData = {
  psycho_score: 9,
  cardImage: '',
  typography: {},
  color_scheme: {},
  design_elements: {},
  patrick_critique: "Perfect card."
}

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

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);

    try {
      // create FormData to send the image file
      const formData = new FormData();
      formData.append('file', selectedFile);

      // call your FastAPI backend
      const response = await fetch('http://localhost:8000/api/analyze/psycho-score', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Backend error:', errorText);
        throw new Error(`Analysis failed: ${response.status}`);
      }

      const data = await response.json();
      console.log('Backend response:', data);

      // wait 3 seconds for the dramatic effect, then navigate
      setTimeout(() => {
        setIsAnalyzing(false);

        // navigate to results page with the analysis data from backend
        navigate('/results', {
          state: {
            analysisData: {
              cardImage: data.cardImage || URL.createObjectURL(selectedFile),
              psycho_score: data.psycho_score || 0,
              card_quality: data.card_quality || 'Not analyzed',
              design_elements: data.design_elements || {},
              typography: data.typography || {},
              color_scheme: data.color_scheme || {},
              layout_quality: data.layout_quality || 'Not analyzed',
              material_impression: data.material_impression || 'Not analyzed',
              patrick_critique: data.patrick_critique || 'Analysis not available',
              audio_url: data.audio_url || null
            }
          }
        });
      }, 3000);

    } catch (error) {
      console.error('Error analyzing card:', error);
      setIsAnalyzing(false);
      alert('Failed to analyze card. Please try again.');
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
            <a href="#" className="nav-link" onClick={() => navigate('/leaderboard')}>LEADERBOARD</a>
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