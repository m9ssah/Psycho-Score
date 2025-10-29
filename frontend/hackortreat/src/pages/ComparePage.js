import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ComparePage.css';

export default function ComparePage() {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Get the first card data from previous page (if coming from results)
  const [card1] = useState(location.state?.cardData || null);
  const [card2, setCard2] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleCard2Upload = async (file) => {
    if (!file) return;

    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/analyze-card', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      
      setCard2({
        cardImage: data.cardImage || URL.createObjectURL(file),
        psycho_score: data.psycho_score,
        card_quality: data.card_quality,
        design_elements: data.design_elements,
        typography: data.typography,
        color_scheme: data.color_scheme,
        layout_quality: data.layout_quality,
        material_impression: data.material_impression,
        patrick_critique: data.patrick_critique
      });

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

  const handleInitiateComparison = () => {
    if (card1 && card2) {
      // Navigate to detailed comparison results page
      navigate('/comparison-results', {
        state: { card1, card2 }
      });
    }
  };

  // Mock data for demonstration (remove when you have real card1 data)
  const displayCard1 = card1 || {
    cardImage: '/placeholder-card.jpg',
    psycho_score: 9.2,
    card_quality: "Impressive. Very nice.",
    patrick_critique: "The tasteful thickness of it. The subtle off-white coloring. A watermark is present, though barely perceptible. The choice of Silian Rail for the typeface demonstrates a refined, yet understated confidence."
  };

  return (
    <div className="comparison-container">
      <div className="comparison-content">
        {/* Header */}
        <div className="comparison-header">
          <h1 className="comparison-title">Comparative Analysis</h1>
          <p className="comparison-subtitle">
            Who is the Alpha? Who is the Beta? Let's put it to the test...
          </p>
        </div>

        {/* Two Column Comparison */}
        <div className="comparison-grid">
          {/* Left Side - The Challenger */}
          <div className="card-column">
            <h2 className="card-column-title">The Challenger</h2>
            
            <div className="card-display-box">
              {displayCard1.cardImage ? (
                <img 
                  src={displayCard1.cardImage} 
                  alt="Challenger Card" 
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
                <span className="evaluation-score">{displayCard1.psycho_score}<span className="score-max">/10</span></span>
              </div>
              
              <h3 className="evaluation-verdict">{displayCard1.card_quality}</h3>
              
              <p className="evaluation-text">
                {displayCard1.patrick_critique}
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
                    <span className="evaluation-score">{card2.score}<span className="score-max">/10</span></span>
                  </div>
                  
                  <h3 className="evaluation-verdict">
                    {card2.score > displayCard1.score ? "Superior craftsmanship." : 
                     card2.score === displayCard1.score ? "Equally matched." : 
                     "Falls short."}
                  </h3>
                  
                  <p className="evaluation-text">
                    {card2.finalImpression}
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