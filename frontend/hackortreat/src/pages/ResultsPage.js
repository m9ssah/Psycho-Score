import React from 'react';
import './ResultsPage.css'
import { useNavigate } from 'react-router-dom';


export default function ResultsPage() {
    const Navigate = useNavigate(); 

    // TODO: REPLACE WITH ACTUAL DATA
    const analysisData = {
      cardImage: '/path-to-card-image.jpg', 
      score: 8.5,
      typography: "The subtle off-white coloring. The tasteful thickness of it. Oh my God, it even has a watermark. Raised lettering, pale nimbus... The choice of Garamond is both classic and assertive. It whispers of old money and quiet confidence. Acceptable.",
      stock: "This feels like \"bone.\" A quality stock. It's not quite Silian Rail, but it has a satisfying heft. One could almost hear the satisfying *thwack* it would make on a boardroom table. It communicates a certain... permanence.",
      layout: "The spacing is precise. Clinical, even. Every element has its place, a testament to a meticulous, perhaps obsessive, attention to detail. The whitespace is not empty; it's a statement. It isolates, it elevates. It's perfect.",
      finalImpression: "A fine piece of work. It conveys power without being ostentatious. It's a card that gets you a reservation at Dorsia. But let's see how it compares to the competition. The game is never truly over."
    };
  
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
              <p className="verdict-quote">"Let's see what we have here..."</p> 
            </div>
  
            {/* Two Column Layout */}
            <div className="results-grid">
              {/* Left Column - Card Image and Score */}
              <div className="left-column">
                <div className="card-preview">
                  <div className="card-image-placeholder">
                    {/* This will be replaced with actual uploaded card image */}
                    <div className="placeholder-text">BUSINESS CARD</div>
                  </div>
                </div>
  
                <div className="score-section">
                  <div className="score-number">{analysisData.score}</div>
                  <div className="score-denominator">/ 10</div>
                </div>
  
                <p className="paul-allen-quote">
                  Impressive. Very nice. Better than Paul Allen's card. 
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
              <button 
              className="btn-secondary"
              onClick={() => Navigate("/")}
              >ANALYZE ANOTHER</button>
              <button 
              className="btn-primary"
              onClick={()=> Navigate("/leaderboard")}
              >SUBMIT TO LEADERBOARD</button>
            </div>
          </div>
        </main>
      </div>
    );
}