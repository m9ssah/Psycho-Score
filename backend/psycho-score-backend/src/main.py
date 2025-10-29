from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from http import HTTPStatus
import os
from PIL import Image
import io
import base64

# Import your existing routers and services
from routers import analyze, audio
from config.settings import settings
from services.gemini_service import gemini_service  # YOUR GEMINI SERVICE

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
    allow_origins=["http://localhost:3000", "http://localhost"],  # Your React app
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


@app.get("/", response_class=HTMLResponse)
def root():
    """Patrick Bateman themed welcome message"""
    html_content = """<!DOCTYPE html>
    <html>
    <head><title>Psycho Score API</title></head>
    <body>
        <h1>🎭 Psycho Score API</h1>
        <p>Patrick Bateman's Business Card Analysis Service</p>
        <a href="/docs">API Documentation</a>
    </body>
    </html>"""
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
            "battle": "/api/analyze/alpha-vs-beta",
            "audio": "/api/audio/generate",
            "docs": "/docs",
        },
    }


# DIRECT ENDPOINT WITH REAL GEMINI INTEGRATION
@app.post("/api/analyze/psycho-score")
async def quick_analysis_endpoint(file: UploadFile = File(...)):
    """
    Quick business card analysis using Gemini AI
    Accept image file, analyze with Gemini, return Patrick's critique
    """
    try:
        # Read the uploaded file
        content = await file.read()
        
        # Validate it's an image
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail="Only image files are supported"
            )
        
        # Open image for base64 encoding
        image = Image.open(io.BytesIO(content))
        
        # Convert image to base64 for returning to frontend
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Reset file pointer for Gemini service
        file.file = io.BytesIO(content)
        
        # CALL YOUR ACTUAL GEMINI SERVICE
        analysis = await gemini_service.analyze_business_card(file)
        
        # Convert Pydantic model to dict and add the card image
        analysis_dict = analysis.dict()
        analysis_dict["cardImage"] = f"data:image/jpeg;base64,{img_base64}"
        
        # Return JSONResponse with explicit status code
        return JSONResponse(
            content=analysis_dict,
            status_code=HTTPStatus.OK  # 200
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )


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
            "POST /api/analyze/alpha-vs-beta": "🥊 BATTLE: Upload two cards → Patrick decides ALPHA vs BETA + audio verdict",
            "POST /api/audio/generate": "🎵 Generate audio from text",
            "GET /api/audio/voices": "🎤 List available voices",
        },
    }