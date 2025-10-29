import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ResultsPage.css';

export default function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get the analysis data passed from the previous page
    if (location.state?.analysisData) {
      setAnalysisData(location.state.analysisData);
      setLoading(false);
    } else {
      // If no data, redirect back to upload page
      navigate('/business-card');
    }
  }, [location, navigate]);

  // Get score-based content
  const getScoreBasedContent = (score) => {
    if (score > 7.5) {
      return {
        quote: '"I have to return some videotapes."',
        paulAllenText: "Impressive. Very nice. Better than Paul Allen's card.",
        scoreColor: '#2d5016', // Dark green
        borderColor: '#2d5016'
      };
    } else if (score >= 5 && score <= 7.5) {
      return {
        quote: '"Let\'s see what we have here..."',
        paulAllenText: "It's acceptable. Decent enough for most occasions, though it lacks... sophistication.",
        scoreColor: '#8b6914', // Gold/amber
        borderColor: '#8b6914'
      };
    } else {
      return {
        quote: '"Is that a gram?"',
        paulAllenText: "Embarrassing. I wouldn't even use this to get into a McDonald's. Back to the drawing board.",
        scoreColor: '#a41e32', // Red
        borderColor: '#a41e32'
      };
    }
  };

  const handleCompareAnother = () => {
    navigate('/business-card');
  };

  const handleSubmitToLeaderboard = () => {
    // TODO: Implement leaderboard submission
    alert('Submitting to leaderboard...');
  };

  if (loading) {
    return (
      <div className="results-container">
        <div className="loading-screen">
          <p>Loading results...</p>
        </div>
      </div>
    );
  }

  const scoreContent = getScoreBasedContent(analysisData.score);

  return (
    <div className="results-container">
      {/* Header */}
      <header className="results-header">
        <div className="results-header-content">
          <h1 className="results-logo">P. BATEMAN & CO.</h1>
          <nav className="results-nav">
            <a href="/business-card" className="results-nav-link">APPRAISAL</a>
            <a href="#" className="results-nav-link">PORTFOLIO</a>
            <a href="#" className="results-nav-link">LEADERBOARD</a>
            <a href="#" className="results-nav-link">CONTACT</a>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="results-main">
        <div className="results-content">
          {/* Title Section */}
          <div className="verdict-section">
            <h2 className="verdict-title">The Verdict</h2>
            <p className="verdict-quote">{scoreContent.quote}</p>
          </div>

          {/* Two Column Layout */}
          <div className="results-grid">
            {/* Left Column - Card Image and Score */}
            <div className="left-column">
              <div className="card-preview">
                {analysisData.cardImage ? (
                  <img 
                    src={analysisData.cardImage} 
                    alt="Business Card" 
                    className="card-image"
                  />
                ) : (
                  <div className="card-image-placeholder">
                    <div className="placeholder-text">BUSINESS CARD</div>
                  </div>
                )}
              </div>

              <div 
                className="score-section" 
                style={{ borderColor: scoreContent.borderColor }}
              >
                <div 
                  className="score-number"
                  style={{ color: scoreContent.scoreColor }}
                >
                  {analysisData.score}
                </div>
                <div className="score-denominator">/ 10</div>
              </div>

              <p className="paul-allen-quote">
                {scoreContent.paulAllenText}
              </p>
            </div>

            {/* Right Column - Critiques */}
            <div className="right-column">
              <div className="critique-item">
                <h3 className="critique-title">CRITIQUE: TYPOGRAPHY</h3>
                <p className="critique-text">{analysisData.typography}</p>
              </div>

              <div className="critique-item">
                <h3 className="critique-title">CRITIQUE: STOCK & TEXTURE</h3>
                <p className="critique-text">{analysisData.stock}</p>
              </div>

              <div className="critique-item">
                <h3 className="critique-title">CRITIQUE: LAYOUT & SPACING</h3>
                <p className="critique-text">{analysisData.layout}</p>
              </div>

              <div className="critique-item">
                <h3 className="critique-title">FINAL IMPRESSION</h3>
                <p className="critique-text">{analysisData.finalImpression}</p>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="action-buttons">
            <button className="btn-secondary" onClick={handleCompareAnother}>
              COMPARE ANOTHER
            </button>
            <button className="btn-primary" onClick={handleSubmitToLeaderboard}>
              SUBMIT TO LEADERBOARD
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}