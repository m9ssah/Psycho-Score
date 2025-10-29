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


# Add startup event to verify routes
@app.on_event("startup")
async def startup_event():
    print("🎭 Psycho Score API starting up...")
    print("Available routes:")
    for route in app.routes:
        print(
            f"   {route.methods if hasattr(route, 'methods') else 'MOUNT'} {route.path}"
        )
    print("API is ready for business card analysis!")


# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static file directories
os.makedirs(settings.AUDIO_OUTPUT_PATH, exist_ok=True)
os.makedirs(settings.IMAGE_UPLOAD_PATH, exist_ok=True)

# Include routers BEFORE mounting static files to avoid conflicts
app.include_router(
    analyze.router, prefix="/api/analyze", tags=["Business Card Analysis"]
)
app.include_router(audio.router, prefix="/api/audio", tags=["Text-to-Speech"])

# Mount static files after API routes
app.mount("/audio", StaticFiles(directory=settings.AUDIO_OUTPUT_PATH), name="audio")
app.mount("/images", StaticFiles(directory=settings.IMAGE_UPLOAD_PATH), name="images")


@app.get("/", response_class=HTMLResponse)  # DELETE THIS LATER
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
                <h3>🎭 Main Endpoint:</h3>
                <p><strong>POST /api/analyze/psycho-score</strong> - Upload business card → Get Patrick's critique + audio</p>
                <br>
                <h3>Other Endpoints:</h3>
                <p><strong>📊 Quick Analysis:</strong> <a href="/api/analyze/quick-analysis">/api/analyze/quick-analysis</a></p>
                <p><strong>🎵 Audio Only:</strong> <a href="/api/audio/generate">/api/audio/generate</a></p>
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
            "analysis": "/api/analyze/psycho-score",
            "quick_analysis": "/api/analyze/quick-analysis",
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
            "POST /api/analyze/psycho-score": "🎭 Main endpoint: Upload business card → Get Patrick's analysis + audio",
            "POST /api/analyze/quick-analysis": "⚡ Quick analysis without audio generation",
            "POST /api/audio/generate": "🎵 Generate audio from text",
            "GET /api/audio/voices": "🎤 List available voices",
        },
    }
