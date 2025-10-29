// API service for Psycho Score Backend
const API_BASE_URL = 'http://localhost:8000';

class PsychoScoreAPI {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    /**
     * Analyze a single business card
     * @param {File} file - The business card image file
     * @returns {Promise} Analysis result with Patrick's critique and audio
     */
    async analyzeSingleCard(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${this.baseURL}/api/analyze/psycho-score`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Analysis failed: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();

            // Transform backend response to frontend format
            return {
                psycho_score: data.psycho_score,
                patrick_critique: data.patrick_critique,
                audio_url: data.audio_url,
                cardImage: URL.createObjectURL(file), // Create preview URL
                // Analysis details
                card_quality: this.getCardQuality(data.psycho_score),
                design_elements: data.analysis_details?.design_elements || {},
                typography: data.analysis_details?.typography || {},
                color_scheme: data.analysis_details?.color_scheme || {},
                layout_quality: data.analysis_details?.layout_quality || 'Standard',
                material_impression: data.analysis_details?.material_impression || 'Professional'
            };
        } catch (error) {
            console.error('Error analyzing card:', error);
            throw error;
        }
    }

    /**
     * Quick analysis without audio generation
     * @param {File} file - The business card image file
     * @returns {Promise} Quick analysis result
     */
    async quickAnalysis(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${this.baseURL}/api/analyze/quick-analysis`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Quick analysis failed: ${response.status}`);
            }

            const data = await response.json();

            return {
                psycho_score: data.psycho_score,
                patrick_critique: data.patrick_critique,
                cardImage: URL.createObjectURL(file),
                card_quality: this.getCardQuality(data.psycho_score)
            };
        } catch (error) {
            console.error('Error in quick analysis:', error);
            throw error;
        }
    }

    /**
     * ALPHA vs BETA battle analysis
     * @param {File} originalCard - The original business card
     * @param {File} contenderCard - The contender's business card
     * @returns {Promise} Battle result with verdict and audio
     */
    async battleAnalysis(originalCard, contenderCard) {
        const formData = new FormData();
        formData.append('original', originalCard);
        formData.append('contender', contenderCard);

        try {
            const response = await fetch(`${this.baseURL}/api/analyze/alpha-vs-beta`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Battle analysis failed: ${response.status}`);
            }

            const data = await response.json();

            return {
                // Battle result
                verdict: data.battle_result?.verdict, // 'ALPHA' or 'BETA'
                winner: data.battle_result?.winner, // 'original' or 'contender'
                announcement: data.battle_result?.announcement,
                audio_url: data.battle_result?.audio_url,

                // Detailed analysis
                original_analysis: {
                    ...data.detailed_analysis?.original_card,
                    cardImage: URL.createObjectURL(originalCard),
                    psycho_score: data.scores?.original_score
                },
                contender_analysis: {
                    ...data.detailed_analysis?.contender_card,
                    cardImage: URL.createObjectURL(contenderCard),
                    psycho_score: data.scores?.contender_score
                },

                // Patrick's comparison
                patrick_comparison: data.detailed_analysis?.patrick_comparison,
                winner_reasoning: data.detailed_analysis?.winner_reasoning,

                // Scores
                scores: data.scores
            };
        } catch (error) {
            console.error('Error in battle analysis:', error);
            throw error;
        }
    }

    /**
     * Generate audio from text
     * @param {string} text - Text to convert to speech
     * @returns {Promise} Audio generation result
     */
    async generateAudio(text) {
        const formData = new FormData();
        formData.append('text', text);

        try {
            const response = await fetch(`${this.baseURL}/api/audio/generate`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Audio generation failed: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error generating audio:', error);
            throw error;
        }
    }

    /**
     * Get available voices
     * @returns {Promise} List of available voices
     */
    async getAvailableVoices() {
        try {
            const response = await fetch(`${this.baseURL}/api/audio/voices`);

            if (!response.ok) {
                throw new Error(`Failed to fetch voices: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching voices:', error);
            throw error;
        }
    }

    /**
     * Health check
     * @returns {Promise} API health status
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            throw error;
        }
    }

    /**
     * Get audio file URL
     * @param {string} audioPath - Audio file path from API response
     * @returns {string} Full URL to audio file
     */
    getAudioURL(audioPath) {
        if (!audioPath) return null;
        return `${this.baseURL}${audioPath}`;
    }

    /**
     * Convert psycho score to quality description
     * @param {number} score - Psycho score (0-10)
     * @returns {string} Quality description
     */
    getCardQuality(score) {
        if (score >= 9) return "Exquisite sophistication";
        if (score >= 8) return "Superior craftsmanship";
        if (score >= 7) return "Refined execution";
        if (score >= 6) return "Professional standard";
        if (score >= 5) return "Adequate presentation";
        if (score >= 4) return "Below expectations";
        if (score >= 3) return "Amateur execution";
        return "Disappointing mediocrity";
    }
}

// Create and export singleton instance
const psychoScoreAPI = new PsychoScoreAPI();
export default psychoScoreAPI;