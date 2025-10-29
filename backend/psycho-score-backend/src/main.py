from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from routers import analyze, audio
from config.settings import settings

# Create FastAPI app with American Psycho themed metadata
app = FastAPI(
    title="Psycho Score API",
    description="Patrick Bateman's Business Card Analysis Service - Where attention to detail meets obsessive perfection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static file directories
if os.path.exists(settings.AUDIO_OUTPUT_PATH):
    app.mount("/audio", StaticFiles(directory=settings.AUDIO_OUTPUT_PATH), name="audio")

if os.path.exists(settings.IMAGE_UPLOAD_PATH):
    app.mount(
        "/images", StaticFiles(directory=settings.IMAGE_UPLOAD_PATH), name="images"
    )

# Include routers
app.include_router(
    analyze.router, prefix="/api/analyze", tags=["Business Card Analysis"]
)
app.include_router(audio.router, prefix="/api/audio", tags=["Text-to-Speech"])


@app.get("/", response_class=HTMLResponse)
def root():
    """
    Patrick Bateman themed welcome message
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Psycho Score API</title>
        <style>
            body { 
                font-family: 'Times New Roman', serif; 
                background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
                color: #f5f5f5; 
                text-align: center; 
                padding: 50px;
                margin: 0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(0,0,0,0.8);
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            }
            h1 { 
                color: #c9a96e; 
                font-size: 2.5em; 
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            }
            .quote {
                font-style: italic;
                font-size: 1.2em;
                color: #d4af37;
                margin: 30px 0;
                border-left: 4px solid #c9a96e;
                padding-left: 20px;
            }
            .api-info {
                background: rgba(201, 169, 110, 0.1);
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }
            a {
                color: #c9a96e;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                color: #d4af37;
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 Psycho Score API</h1>
            <div class="quote">
                "Look at that subtle off-white coloring. The tasteful thickness of it. 
                Oh my God, it even has a watermark."
            </div>
            <p>Welcome to the most sophisticated business card analysis service ever created.</p>
            <div class="api-info">
                <h3>Available Endpoints:</h3>
                <p><strong>📊 Analysis:</strong> <a href="/api/analyze/business-card">/api/analyze/business-card</a></p>
                <p><strong>🎵 Audio:</strong> <a href="/api/audio/generate">/api/audio/generate</a></p>
                <p><strong>📖 Documentation:</strong> <a href="/docs">/docs</a></p>
            </div>
            <p><em>Where obsessive attention to detail meets cutting-edge AI technology.</em></p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    return {
        "status": "healthy",
        "service": "Psycho Score API",
        "version": "1.0.0",
        "patrick_says": "The sophistication of this API is... breathtaking.",
        "endpoints": {
            "analysis": "/api/analyze/business-card",
            "audio": "/api/audio/generate",
            "docs": "/docs",
        },
    }


@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "title": "Psycho Score API",
        "description": "Patrick Bateman's Business Card Analysis Service",
        "version": "1.0.0",
        "features": [
            "AI-powered business card analysis",
            "Patrick Bateman style critiques",
            "Text-to-speech with character voice",
            "Detailed design assessment",
        ],
        "endpoints": {
            "POST /api/analyze/business-card": "Complete business card analysis with optional audio",
            "POST /api/analyze/image-only": "Image analysis without audio generation",
            "POST /api/audio/generate": "Generate audio from text",
            "POST /api/audio/patrick-critique": "Generate Patrick Bateman style audio critique",
            "GET /api/audio/voices": "List available voices",
        },
    }
