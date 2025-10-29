# 🎭 Psycho Score Backend

*"Look at that subtle off-white coloring. The tasteful thickness of it. Oh my God, it even has a watermark."*

A FastAPI backend service that channels Patrick Bateman's obsessive attention to detail to analyze business cards with AI-powered sophistication.

## 🎯 Features

### Core Functionality
- **AI-Powered Analysis**: Uses Google Gemini Vision API to analyze business card design elements
- **Patrick Bateman Voice**: Generates critiques in the characteristic style of American Psycho's protagonist
- **Text-to-Speech**: ElevenLabs integration for authentic Patrick Bateman audio delivery
- **Comprehensive Scoring**: Detailed assessment covering typography, color, layout, and materials

### Technical Features
- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **Async Processing**: Non-blocking operations for optimal performance
- **Image Processing**: PIL-based image enhancement and validation
- **Error Handling**: Comprehensive error responses with detailed feedback
- **CORS Support**: Configured for seamless frontend integration
- **Static File Serving**: Serves generated audio files and uploaded images

## 🏗️ Architecture

```
src/
├── main.py                 # FastAPI application entry point
├── config/
│   ├── __init__.py
│   └── settings.py         # Configuration and environment variables
├── models/
│   ├── __init__.py
│   └── schemas.py          # Pydantic models for request/response validation
├── routers/
│   ├── __init__.py
│   ├── analyze.py          # Business card analysis endpoints
│   └── audio.py            # Text-to-speech endpoints
├── services/
│   ├── __init__.py
│   ├── gemini_service.py   # Google Gemini Vision API integration
│   └── elevenlabs_service.py # ElevenLabs TTS API integration
└── utils/
    ├── __init__.py
    └── image_processing.py # Image validation and processing utilities
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key
- ElevenLabs API key

### Installation

1. **Clone and navigate to backend directory**
```bash
cd backend/psycho-score-backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
PATRICK_VOICE_ID=pNInz6obpgDQGcFmaJgB
```

5. **Create necessary directories**
```bash
mkdir -p uploads/images outputs/audio
```

6. **Run the development server**
```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Analysis Endpoints

#### `POST /api/analyze/business-card`
Complete business card analysis with optional audio generation.

**Parameters:**
- `file`: Business card image (multipart/form-data)
- `include_audio`: Boolean (default: true)
- `voice_id`: Optional ElevenLabs voice ID override

**Response:**
```json
{
  "id": "uuid",
  "analysis": {
    "card_quality": "Exquisite attention to detail...",
    "design_elements": {
      "layout": "Sophisticated asymmetrical composition",
      "whitespace": "Masterful use of negative space",
      "composition": "Harmonious balance of elements"
    },
    "typography": {
      "font_family": "Elegant serif with modern sans-serif accent",
      "hierarchy": "Clear typographic hierarchy",
      "readability": "Exceptional legibility"
    },
    "color_scheme": {
      "palette": "Subtle off-white with tasteful accents",
      "contrast": "Perfect contrast ratios",
      "sophistication": "Understated elegance"
    },
    "layout_quality": "Flawless execution",
    "material_impression": "Premium card stock with subtle texture",
    "patrick_critique": "The subtle off-white coloring...",
    "psycho_score": 9.2
  },
  "audio": {
    "audio_url": "/audio/psycho_analysis_xyz.mp3",
    "file_size": 245760
  },
  "created_at": "2024-01-15T10:30:00Z",
  "processing_time": 3.45
}
```

## 🔧 Configuration

### Environment Variables
```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key

# Voice Configuration
PATRICK_VOICE_ID=pNInz6obpgDQGcFmaJgB

# File Handling
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_IMAGE_TYPES=["image/jpeg", "image/png", "image/jpg"]

# Directories
IMAGE_UPLOAD_PATH=uploads/images
AUDIO_OUTPUT_PATH=outputs/audio
```

## � Web Deployment

The backend is optimized for web deployment platforms:

### **Vercel (Recommended)**
```bash
npm i -g vercel
vercel --prod
```

### **Railway**
```bash
npm install -g @railway/cli
railway login
railway deploy
```

### **Render**
- Connect your GitHub repository
- Build command: `pip install -r requirements.txt`
- Start command: `cd src && uvicorn main:app --host 0.0.0.0 --port $PORT`

## �📦 Dependencies

### Core
- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Pillow**: Image processing

### AI Services
- **google-generativeai**: Gemini Vision API
- **httpx**: Async HTTP client
- **aiofiles**: Async file operations

---

*"I have to return some videotapes... but first, let me analyze your business card."*