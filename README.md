# 🎭 Psycho Score - Business Card Analyzer

> *"Look at that subtle off-white coloring. The tasteful thickness of it. Oh my God... it even has a watermark."*

A fun, American Psycho-inspired web application that analyzes business cards with Patrick Bateman's obsessive attention to detail. Built as a playful exploration of AI-powered design critique and text-to-speech technologies.

![American Psycho Business Card Scene](https://img.shields.io/badge/Inspired%20By-American%20Psycho-8B0000?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Demo-brightgreen?style=for-the-badge)

---

## 📖 About

**Psycho Score** is a tongue-in-cheek homage to the iconic business card scene from *American Psycho*. This project was created primarily to explore **ElevenLabs' text-to-speech capabilities** and experiment with AI-powered visual analysis, all wrapped in the aesthetic sensibility of Patrick Bateman's neurotic perfectionism.

Upload a business card image, and Patrick (powered by Google's Gemini AI) will scrutinize every detail—from typography and color scheme to material impression—delivering a verdict in his signature style of sophisticated disdain or begrudging approval.

**⚠️ Disclaimer:** This is a fun, experimental project for entertainment and learning purposes. Not intended for serious design critique!

---

## ✨ Features

### 🎨 **AI-Powered Business Card Analysis**
- **Gemini Vision AI** analyzes typography, layout, color scheme, and design elements
- Generates Patrick Bateman-style critiques with obsessive attention to detail
- Assigns a "Psycho Score" from 0-10 based on perceived sophistication

### 🎤 **Text-to-Speech Audio Narration**
- **ElevenLabs API** generates audio of Patrick's critique in character voice
- Brings the analysis to life with dramatic flair
- (Note: Audio generation requires ElevenLabs API key)

### ⚔️ **Card Battle Mode**
- Compare two business cards head-to-head
- Patrick declares one card "ALPHA" and the other "BETA"
- Witness the dramatic verdict with score comparison

### 🎭 **Thematic UI/UX**
- Design inspired by *American Psycho's* 1980s corporate aesthetic
- Dynamic reactions based on card scores (good/mid/bad)
- Vintage serif typography and burgundy color palette
- Patrick Bateman reaction images throughout

---

## 🛠️ Tech Stack

### **Frontend**
- **React** - UI framework
- **React Router** - Navigation
- **CSS3** - Styling with custom themes

### **Backend**
- **FastAPI** - Python web framework
- **Google Gemini API** - Vision AI for card analysis
- **ElevenLabs API** - Text-to-speech generation
- **Pillow (PIL)** - Image processing

### **Architecture**
- RESTful API design
- JSON response formatting
- Base64 image encoding
- CORS-enabled for local development

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** (v16+)
- **Python** (3.8+)
- **Google Gemini API Key** ([Get it here](https://ai.google.dev/))
- **ElevenLabs API Key** (Optional - for audio) ([Get it here](https://elevenlabs.io/))

### Installation

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/psycho-score.git
cd psycho-score
```

#### 2️⃣ Backend Setup
```bash
cd backend/psycho-score-backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_BASE_URL=https://api.elevenlabs.io/v1
PATRICK_VOICE_ID=your_voice_id_here
AUDIO_OUTPUT_PATH=./audio_files
IMAGE_UPLOAD_PATH=./uploaded_images
EOF

# Start the server
cd src
python -m uvicorn main:app --reload
```

Backend will run on: `http://localhost:8000`

#### 3️⃣ Frontend Setup
```bash
cd frontend/hackortreat

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run on: `http://localhost:3000`

---

## 📁 Project Structure

```
psycho-score/
├── backend/
│   └── psycho-score-backend/
│       └── src/
│           ├── main.py                    # FastAPI app entry point
│           ├── routers/
│           │   ├── analyze.py             # Card analysis endpoints
│           │   └── audio.py               # Audio generation endpoints
│           ├── services/
│           │   ├── gemini_service.py      # Gemini AI integration
│           │   └── elevenlabs_service.py  # ElevenLabs TTS
│           ├── models/
│           │   └── schemas.py             # Pydantic models
│           └── config/
│               └── settings.py            # Environment config
├── frontend/
│   └── hackortreat/
│       └── src/
│           ├── pages/
│           │   ├── HomePage.js            # Card upload
│           │   ├── ResultsPage.js         # Analysis results
│           │   ├── ComparePage.js         # Battle mode
│           │   ├── AlphaPage.js           # Victory page
│           │   └── BetaPage.js            # Defeat page
│           ├── assets/                    # Patrick Bateman images
│           └── App.js                     # Main router
└── README.md
```

---

## 🎮 Usage

### Single Card Analysis
1. Navigate to the home page
2. Upload a business card image (PNG, JPG)
3. Click **"ANALYZE CARD"**
4. Wait for Patrick's dramatic analysis (3 seconds + AI processing)
5. View your **Psycho Score** and detailed critique

### Battle Mode
1. Analyze your first card
2. Click **"COMPARE CARDS"**
3. Upload a second card
4. Click **"INITIATE COMPARISON"**
5. Discover who's **ALPHA** and who's **BETA**

---

## 📊 API Endpoints

### Analysis
- `POST /api/analyze/psycho-score` - Full analysis with audio
- `POST /api/analyze/quick-analysis` - Analysis without audio
- `POST /api/analyze/alpha-vs-beta` - Compare two cards

### Audio
- `POST /api/audio/generate` - Generate TTS audio
- `GET /api/audio/voices` - List available voices

### Health
- `GET /health` - API health check
- `GET /docs` - Interactive API documentation

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🎬 Credits

**Inspiration:**
- *American Psycho* (2000) directed by Mary Harron
- Based on the novel by Bret Easton Ellis

**Technologies:**
- [Google Gemini AI](https://ai.google.dev/)
- [ElevenLabs](https://elevenlabs.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)

**Created by:** Massah Arafeh, Jemima Silaen, Julia Sinclair 

---

Made with ❤️ (and mild neurosis) as a tribute to Patrick Bateman's impeccable taste.
