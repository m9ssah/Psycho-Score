import React, { useEffect, useState } from 'react';
import './ResultsPage.css';
import { useNavigate, useLocation } from 'react-router-dom';

// fake card data
const analysisData = {
    cardImage: '/path-to-card-image.jpg', 
    score: 8.5,
    typography: "The subtle off-white coloring. The tasteful thickness of it. Oh my God, it even has a watermark. Raised lettering, pale nimbus... The choice of Garamond is both classic and assertive. It whispers of old money and quiet confidence. Acceptable.",
    stock: "This feels like \"bone.\" A quality stock. It's not quite Silian Rail, but it has a satisfying heft. One could almost hear the satisfying *thwack* it would make on a boardroom table. It communicates a certain... permanence.",
    layout: "The spacing is precise. Clinical, even. Every element has its place, a testament to a meticulous, perhaps obsessive, attention to detail. The whitespace is not empty; it's a statement. It isolates, it elevates. It's perfect.",
    finalImpression: "A fine piece of work. It conveys power without being ostentatious. It's a card that gets you a reservation at Dorsia. But let's see how it compares to the competition. The game is never truly over."
  };

export default function ResultsPage() {
    const navigate = useNavigate(); 
    const location = useLocation();
    const [analysisData, setAnalysisData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Get the analysis data passed from the previous page
        if (location.state?.analysisData) {
          setAnalysisData(location.state.analysisData);
          setLoading(false);
        } else {
          // If no data, redirect back to upload page
          navigate('/');
        }
      }, [location, navigate]);

    // Get score-based content (>7.5 good, 5-7.5 mid, <5 bad)
    const getScoreBasedContent = (score) => {
        if (score >= 7.5) {
        return {
            quote: '"Oh my God. It even has a watermark."',
            scoreColor: '#2d5016', // Dark green
            borderColor: '#2d5016'
        };
        } else if (score >= 5 && score < 7.5) {
        return {
            quote: '"Acceptable. Highly competent, yes, but does it possess that subtle off-white coloring?"',
            scoreColor: '#8b6914', // Gold/amber
            borderColor: '#8b6914'
        };
        } else {
        return {
            quote: '"Embarassing. I wouldn\'t use it at Dorsia."',
            scoreColor: '#a41e32', // Red
            borderColor: '#a41e32'
        };
        }
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

    const scoreContent = getScoreBasedContent(analysisData.psycho_score);

    return (
        <div className="results-container">
          {/* Header */}
          <header className="results-header">
            <div className="results-header-content">
              <h1 className="results-logo">P. BATEMAN & CO.</h1>
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
                      {analysisData.psycho_score}
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
                    <p className="critique-text">
                      <strong>Font Family:</strong> {analysisData.typography.font_family}<br />
                      <strong>Hierarchy:</strong> {analysisData.typography.hierarchy}<br />
                      <strong>Readability:</strong> {analysisData.typography.readability}
                    </p>
                  </div>
    
                  <div className="critique-item">
                    <h3 className="critique-title">CRITIQUE: COLOR & MATERIAL</h3>
                    <p className="critique-text">
                      <strong>Palette:</strong> {analysisData.color_scheme.palette}<br />
                      <strong>Contrast:</strong> {analysisData.color_scheme.contrast}<br />
                      <strong>Material:</strong> {analysisData.material_impression}
                    </p>
                  </div>
    
                  <div className="critique-item">
                    <h3 className="critique-title">CRITIQUE: LAYOUT & DESIGN</h3>
                    <p className="critique-text">
                      <strong>Layout:</strong> {analysisData.design_elements.layout}<br />
                      <strong>Whitespace:</strong> {analysisData.design_elements.whitespace}<br />
                      <strong>Composition:</strong> {analysisData.design_elements.composition}
                    </p>
                  </div>
    
                  <div className="critique-item">
                    <h3 className="critique-title">PATRICK'S FINAL THOUGHTS</h3>
                    <p className="critique-text patrick-critique">
                      {analysisData.patrick_critique}
                    </p>
                  </div>
                </div>
              </div>
    
              {/* Action Buttons */}
              <div className="action-buttons">
                <button 
                  className="btn-secondary"
                  onClick={() => {navigate("/")}}
                >
                  ANALYZE ANOTHER
                </button>
                <button 
                  className="btn-secondary"
                  onClick={() => {navigate("/compare")}}
                >
                  COMPARE CARD
                </button>
              </div>
            </div>
          </main>
        </div>
      );
    }