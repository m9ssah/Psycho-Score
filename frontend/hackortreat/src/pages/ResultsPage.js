import React, { useEffect, useState } from 'react';
import './ResultsPage.css';
import { useNavigate, useLocation } from 'react-router-dom';
import psychoScoreAPI from '../services/api';

// Import bateman images
import batemanGood1 from '../assets/bateman-good1.jpg';
import batemanGood2 from '../assets/bateman-good2.jpg';
import batemanGood3 from '../assets/bateman-good3.jpg';
import batemanMid1 from '../assets/bateman-mid1.jpg';
import batemanMid2 from '../assets/bateman-mid2.jpg';
import batemanBad1 from '../assets/bateman-bad1.jpg';
import batemanBad2 from '../assets/bateman-bad2.jpg';

export default function ResultsPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioError, setAudioError] = useState(null);

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

  // Get score-based content (>7.5 good, 5-7.5 mid, <5 bad)
  const getScoreBasedContent = (score) => {
    let batemanImage;

    // Select random bateman image based on score
    if (score >= 7.5) {
      const goodImages = [batemanGood1, batemanGood2, batemanGood3];
      batemanImage = goodImages[Math.floor(Math.random() * goodImages.length)];
    } else if (score >= 5 && score < 7.5) {
      const midImages = [batemanMid1, batemanMid2];
      batemanImage = midImages[Math.floor(Math.random() * midImages.length)];
    } else {
      const badImages = [batemanBad1, batemanBad2];
      batemanImage = badImages[Math.floor(Math.random() * badImages.length)];
    }

    if (score > 7.5) {
      return {
        quote: '"I\'ll be seeing you at Dorsia."',
        paulAllenText: "Impressive. Very nice. Better than Paul Allen's card.",
        scoreColor: '#2d5016', // Dark green
        borderColor: '#2d5016',
        batemanImage: batemanImage
      };
    } else if (score >= 5 && score <= 7.5) {
      return {
        quote: '"Let\'s see what we have here..."',
        paulAllenText: "It's acceptable. Decent enough for most occasions, though it lacks... sophistication.",
        scoreColor: '#8b6914', // Gold/amber
        borderColor: '#8b6914',
        batemanImage: batemanImage
      };
    } else {
      return {
        quote: '"And you claim to be an employee here?"',
        paulAllenText: "Embarrassing. Try getting a reservation at Dorsia now!",
        scoreColor: '#a41e32', // Red
        borderColor: '#a41e32',
        batemanImage: batemanImage
      };
    }
  };

  const handleCompareAnother = () => {
    // Pass the FULL analysis data to compare page
    navigate('/compare', {
      state: {
        cardData: analysisData // This includes all the fields from backend
      }
    });
  };

  const handlePlayAudio = () => {
    if (!analysisData.audio_url) {
      setAudioError('No audio available');
      return;
    }

    try {
      const audioUrl = psychoScoreAPI.getAudioURL(analysisData.audio_url);
      const audio = new Audio(audioUrl);

      setIsPlaying(true);
      setAudioError(null);

      audio.onended = () => setIsPlaying(false);
      audio.onerror = () => {
        setIsPlaying(false);
        setAudioError('Failed to play audio');
      };

      audio.play();
    } catch (error) {
      setIsPlaying(false);
      setAudioError('Failed to play audio');
    }
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

          {/* Patrick Bateman Image */}
          <div className="bateman-image-container">
            <img
              src={scoreContent.batemanImage}
              alt="Patrick Bateman"
              className="bateman-reaction-image"
            />
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

                {/* Audio Playback */}
                {analysisData.audio_url && (
                  <div className="audio-section">
                    <button
                      className="play-audio-btn"
                      onClick={handlePlayAudio}
                      disabled={isPlaying}
                    >
                      {isPlaying ? '🔊 Playing...' : '🎤 Hear Patrick\'s Critique'}
                    </button>
                    {audioError && <p className="audio-error">{audioError}</p>}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="action-buttons">
            <button
              className="btn-secondary"
              onClick={handleCompareAnother}
            >
              COMPARE WITH ANOTHER
            </button>
            <button
              className="btn-primary"
              onClick={() => navigate('/')}
            >
              ANALYZE ANOTHER
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}