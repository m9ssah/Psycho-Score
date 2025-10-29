import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './BetaPage.css';

export default function BetaPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [showContent, setShowContent] = useState(false);
  const yourCard = location.state?.yourCard;
  const opponentCard = location.state?.opponentCard;

  useEffect(() => {
    // Dramatic entrance animation
    setTimeout(() => setShowContent(true), 300);
  }, []);

  const handleTryAgain = () => {
    navigate('/compare');
  };

  return (
    <div className="beta-container">
      {/* Animated Background */}
      <div className="beta-bg-animation"></div>
      <div className="beta-grain"></div>

      {/* Main Content */}
      <div className={`beta-content ${showContent ? 'visible' : ''}`}>
        {/* Broken Crown Section */}
        <div className="beta-icon-section">
          <div className="icon-crack"></div>
          <div className="beta-icon">💔</div>
          <div className="icon-shadow"></div>
        </div>

        {/* Main Title */}
        <h1 className="beta-title">
          <span className="beta-word">NOT</span>
          <span className="beta-word">QUITE</span>
          <span className="beta-word beta-word-main">THERE</span>
        </h1>

        {/* Score Comparison */}
        {yourCard && opponentCard && (
          <div className="score-comparison">
            <div className="score-column your-score">
              <div className="score-label">YOUR SCORE</div>
              <div className="score-value losing">{yourCard.psycho_score}</div>
            </div>
            <div className="vs-text">VS</div>
            <div className="score-column opponent-score">
              <div className="score-label">THEIR SCORE</div>
              <div className="score-value winning">{opponentCard.psycho_score}</div>
            </div>
          </div>
        )}

        {/* Harsh Quote */}
        <div className="beta-quote-section">
          <div className="quote-marks">"</div>
          <p className="beta-quote">
            Look at that subtle off-white coloring. The tasteful thickness of it. 
            Oh my God... it even has a watermark. Your card, however... needs work.
          </p>
          <div className="quote-marks">"</div>
        </div>

        {/* Reality Check */}
        <div className="reality-check">
          <div className="reality-border-top"></div>
          <h3 className="reality-title">THE REALITY</h3>
          <p className="reality-text">
            In a world of alphas, you've revealed yourself to be... adequate. 
            Your card lacks the je ne sais quoi that separates the powerful from the pedestrian. 
            The material isn't quite Silian Rail. The font choice betrays uncertainty. 
            The composition whispers of compromise rather than commands respect.
          </p>
          <p className="reality-conclusion">
            Back to the drawing board. Excellence demands more.
          </p>
          <div className="reality-border-bottom"></div>
        </div>

        {/* Deficit Stats */}
        <div className="deficit-stats">
          <div className="deficit-item">
            <div className="deficit-label">SCORE GAP</div>
            <div className="deficit-value">
              -{(opponentCard?.psycho_score - yourCard?.psycho_score).toFixed(1)}
            </div>
          </div>
          <div className="deficit-divider"></div>
          <div className="deficit-item">
            <div className="deficit-label">HIERARCHY</div>
            <div className="deficit-value">BETA</div>
          </div>
          <div className="deficit-divider"></div>
          <div className="deficit-item">
            <div className="deficit-label">DORSIA STATUS</div>
            <div className="deficit-value">DENIED</div>
          </div>
        </div>

        {/* Improvement Areas */}
        <div className="improvement-section">
          <h3 className="improvement-title">AREAS FOR IMPROVEMENT</h3>
          <div className="improvement-grid">
            <div className="improvement-item">
              <div className="improvement-icon">📝</div>
              <div className="improvement-text">Typography lacks authority</div>
            </div>
            <div className="improvement-item">
              <div className="improvement-icon">🎨</div>
              <div className="improvement-text">Color scheme too timid</div>
            </div>
            <div className="improvement-item">
              <div className="improvement-icon">📏</div>
              <div className="improvement-text">Layout needs refinement</div>
            </div>
            <div className="improvement-item">
              <div className="improvement-icon">💎</div>
              <div className="improvement-text">Material quality insufficient</div>
            </div>
          </div>
        </div>

        {/* Bateman's Harsh Verdict */}
        <div className="verdict-box">
          <p className="verdict-text">
            "I have to return some videotapes. And you... you need to return to the printer."
          </p>
          <p className="verdict-signature">— Patrick Bateman</p>
        </div>

        {/* Action Buttons */}
        <div className="beta-actions">
          <button className="beta-btn primary" onClick={handleTryAgain}>
            <span className="btn-glow"></span>
            TRY AGAIN
          </button>
        </div>

        {/* Bottom Motivation */}
        <div className="beta-bottom-text">
          <p>Even Bateman had to start somewhere. Refine. Perfect. Dominate.</p>
        </div>
      </div>

      {/* Falling Particles (failure theme) */}
      <div className="falling-particles">
        {[...Array(15)].map((_, i) => (
          <div key={i} className="falling-particle" style={{
            left: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 2}s`,
            animationDuration: `${2 + Math.random() * 3}s`
          }}></div>
        ))}
      </div>
    </div>
  );
}