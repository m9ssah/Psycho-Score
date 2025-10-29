import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ComparePage.css';
import psychoScoreAPI from '../services/api';

export default function ComparePage() {
  const location = useLocation();
  const navigate = useNavigate();

  const card1 = location.state?.cardData;
  const [card2, setCard2] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  // If no card1, redirect back
  React.useEffect(() => {
    if (!card1) {
      navigate('/');
    }
  }, [card1, navigate]);

  const handleCard2Upload = async (file) => {
    if (!file) return;

    setIsUploading(true);

    try {
      // Use quick analysis for the second card
      const data = await psychoScoreAPI.quickAnalysis(file);

      // Store the analysis data for card2
      setCard2(data);
      setIsUploading(false);
    } catch (error) {
      console.error('Error analyzing card:', error);
      setIsUploading(false);
      alert('Failed to analyze card. Please try again.');
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleCard2Upload(e.target.files[0]);
    }
  };

  const handleReplaceCard1 = () => {
    navigate('/');
  };

  const handleInitiateComparison = async () => {
    if (!card1 || !card2) return;

    try {
      // Get the original files to send to battle API
      const originalFile = await fetch(card1.cardImage).then(r => r.blob());
      const contenderFile = await fetch(card2.cardImage).then(r => r.blob());

      // Call the ALPHA vs BETA battle API
      const battleResult = await psychoScoreAPI.battleAnalysis(originalFile, contenderFile);

      if (battleResult.verdict === 'ALPHA') {
        // Original card wins - YOU ARE ALPHA
        navigate('/alpha', {
          state: {
            battleResult,
            yourCard: card1,
            opponentCard: card2,
            winner: 'you'
          }
        });
      } else {
        // Contender wins - YOU ARE BETA
        navigate('/beta', {
          state: {
            battleResult,
            yourCard: card1,
            opponentCard: card2,
            winner: 'opponent'
          }
        });
      }
    } catch (error) {
      console.error('Battle analysis failed:', error);
      alert('Battle analysis failed. Please try again.');
    }
  };

  if (!card1) {
    return null; // Will redirect in useEffect
  }

  return (
    <div className="comparison-container">
      <div className="comparison-content">
        {/* Header */}
        <div className="comparison-header">
          <h1 className="comparison-title">Comparative Analysis</h1>
          <p className="comparison-subtitle">
            A side-by-side evaluation of aesthetic and material superiority. Let's see who's the alpha.
          </p>
        </div>

        {/* Two Column Comparison */}
        <div className="comparison-grid">
          {/* Left Side - Your Card (The Challenger) */}
          <div className="card-column">
            <h2 className="card-column-title">Your Card</h2>

            <div className="card-display-box">
              {card1.cardImage ? (
                <img
                  src={card1.cardImage}
                  alt="Your Card"
                  className="comparison-card-image"
                />
              ) : (
                <div className="card-placeholder">
                  <div className="placeholder-card-text">BUSINESS CARD</div>
                </div>
              )}
            </div>

            <div className="evaluation-section">
              <div className="evaluation-header">
                <span className="evaluation-label">EVALUATION</span>
                <span className="evaluation-score">
                  {card1.psycho_score}
                  <span className="score-max">/10</span>
                </span>
              </div>

              <h3 className="evaluation-verdict">{card1.card_quality}</h3>

              <p className="evaluation-text">
                {card1.patrick_critique.substring(0, 150)}...
              </p>
            </div>

            <button className="replace-card-btn" onClick={handleReplaceCard1}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
              Replace Card
            </button>
          </div>

          {/* VS Divider */}
          <div className="vs-divider">
            <span className="vs-text">VS</span>
          </div>

          {/* Right Side - The Contender */}
          <div className="card-column contender">
            <h2 className="card-column-title">The Contender</h2>

            {card2 ? (
              <>
                <div className="card-display-box">
                  <img
                    src={card2.cardImage}
                    alt="Contender Card"
                    className="comparison-card-image"
                  />
                </div>

                <div className="evaluation-section">
                  <div className="evaluation-header">
                    <span className="evaluation-label">EVALUATION</span>
                    <span className="evaluation-score">
                      {card2.psycho_score}
                      <span className="score-max">/10</span>
                    </span>
                  </div>

                  <h3 className="evaluation-verdict">
                    {card2.psycho_score > card1.psycho_score ? "Superior craftsmanship." :
                      card2.psycho_score === card1.psycho_score ? "Equally matched." :
                        "Falls short."}
                  </h3>

                  <p className="evaluation-text">
                    {card2.patrick_critique.substring(0, 150)}...
                  </p>
                </div>

                <button className="replace-card-btn" onClick={() => setCard2(null)}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                  </svg>
                  Replace Card
                </button>
              </>
            ) : (
              <div className="upload-contender-box">
                <div className="upload-icon-large">
                  <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="12" y1="8" x2="12" y2="16"></line>
                    <line x1="8" y1="12" x2="16" y2="12"></line>
                  </svg>
                </div>
                <p className="awaiting-text">
                  {isUploading ? 'Analyzing...' : 'Awaiting second card...'}
                </p>
                <label htmlFor="contender-upload">
                  <input
                    id="contender-upload"
                    type="file"
                    className="file-input-hidden"
                    accept="image/*"
                    onChange={handleFileSelect}
                    disabled={isUploading}
                  />
                  <span className="upload-card-btn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                      <polyline points="17 8 12 3 7 8"></polyline>
                      <line x1="12" y1="3" x2="12" y2="15"></line>
                    </svg>
                    Upload Card
                  </span>
                </label>
              </div>
            )}
          </div>
        </div>

        {/* Initiate Comparison Button */}
        <div className="comparison-action">
          <button
            className="initiate-comparison-btn"
            onClick={handleInitiateComparison}
            disabled={!card1 || !card2}
          >
            INITIATE COMPARISON
          </button>
        </div>
      </div>
    </div>
  );
}