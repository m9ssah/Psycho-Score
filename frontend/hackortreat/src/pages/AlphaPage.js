import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './AlphaPage.css';

export default function AlphaPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [showContent, setShowContent] = useState(false);
  const cardData = location.state?.cardData;

  useEffect(() => {
    // Dramatic entrance animation
    setTimeout(() => setShowContent(true), 300);
  }, []);

  const handleViewLeaderboard = () => {
    navigate('/leaderboard');
  };

  const handleAnalyzeAnother = () => {
    navigate('/');
  };

  return (
    <div className="alpha-container">
      {/* Animated Background */}
      <div className="alpha-bg-animation"></div>
      <div className="alpha-grain"></div>

      {/* Main Content */}
      <div className={`alpha-content ${showContent ? 'visible' : ''}`}>
        {/* Crown/Trophy Section */}
        <div className="alpha-trophy-section">
          <div className="trophy-glow"></div>
          <div className="trophy-icon">👑</div>
          <div className="trophy-shine"></div>
        </div>

        {/* Main Title */}
        <h1 className="alpha-title">
          <span className="alpha-word">YOU</span>
          <span className="alpha-word">ARE</span>
          <span className="alpha-word alpha-word-main">ALPHA</span>
        </h1>

        {/* Score Display */}
        {cardData && (
          <div className="alpha-score-display">
            <div className="score-label">PSYCHO SCORE</div>
            <div className="score-massive">{cardData.psycho_score}</div>
            <div className="score-divider"></div>
            <div className="score-perfect">PERFECT 10</div>
          </div>
        )}

        {/* Epic Quote */}
        <div className="alpha-quote-section">
          <div className="quote-marks">"</div>
          <p className="alpha-quote">
            Impressive. Very nice. Let's see Paul Allen try to top this.
          </p>
          <div className="quote-marks">"</div>
        </div>

        {/* Achievement Badges */}
        <div className="achievement-grid">
          <div className="achievement-badge">
            <div className="badge-icon">⚡</div>
            <div className="badge-text">DORSIA<br/>APPROVED</div>
          </div>
          <div className="achievement-badge">
            <div className="badge-icon">💎</div>
            <div className="badge-text">SILIAN RAIL<br/>CERTIFIED</div>
          </div>
          <div className="achievement-badge">
            <div className="badge-icon">🏆</div>
            <div className="badge-text">TOP 1%<br/>ELITE</div>
          </div>
        </div>

        {/* Bateman's Verdict */}
        <div className="alpha-verdict">
          <div className="verdict-border-top"></div>
          <p className="verdict-text">
            The tasteful thickness. The subtle coloring. The watermark. 
            My God... it even has a raised lettering. This is a card that commands respect.
            A card that opens doors. A card that gets you a reservation at Dorsia on a Friday night.
          </p>
          <p className="verdict-signature">— Patrick Bateman</p>
          <div className="verdict-border-bottom"></div>
        </div>

        {/* Stats Row */}
        <div className="alpha-stats">
          <div className="stat-item">
            <div className="stat-number">TOP 1</div>
            <div className="stat-label">LEADERBOARD RANK</div>
          </div>
          <div className="stat-divider"></div>
          <div className="stat-item">
            <div className="stat-number">∞</div>
            <div className="stat-label">CONFIDENCE LEVEL</div>
          </div>
          <div className="stat-divider"></div>
          <div className="stat-item">
            <div className="stat-number">100%</div>
            <div className="stat-label">ALPHA STATUS</div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="alpha-actions">
          {/*<button className="alpha-btn primary" onClick={handleViewLeaderboard}>
            <span className="btn-shine"></span>
            VIEW LEADERBOARD
          </button> */}
          <button className="alpha-btn secondary" onClick={handleAnalyzeAnother}>
            RETURN HOME
          </button>
        </div>

        {/* Bottom Text */}
        <div className="alpha-bottom-text">
          <p>Your business card has been immortalized in the Hall of Excellence</p>
        </div>
      </div>

      {/* Particles Effect */}
      <div className="particles">
        {[...Array(20)].map((_, i) => (
          <div key={i} className="particle" style={{
            left: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 3}s`,
            animationDuration: `${3 + Math.random() * 4}s`
          }}></div>
        ))}
      </div>
    </div>
  );
}