from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import uuid
import time
from typing import Optional
from services.gemini_service import gemini_service
from services.elevenlabs_service import elevenlabs_service
from utils.image_processing import image_processor
from models.schemas import (
    AnalysisResponse,
    BusinessCardAnalysis,
    AudioResponse,
    AnalysisRequest,
    ErrorResponse,
)

router = APIRouter()


@router.post(
    "/business-card",
    response_model=AnalysisResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def analyze_business_card_complete(
    file: UploadFile = File(..., description="Business card image file"),
    include_audio: bool = Form(default=True, description="Generate audio critique"),
    voice_id: Optional[str] = Form(
        default=None, description="ElevenLabs voice ID override"
    ),
):
    """
    Complete business card analysis endpoint - analyzes image and optionally generates Patrick Bateman audio critique
    """
    start_time = time.time()
    analysis_id = str(uuid.uuid4())

    try:
        # Validate image
        image_processor.validate_image(file)

        # Analyze business card with Gemini
        analysis = await gemini_service.analyze_business_card(file)

        # Generate audio if requested
        audio_response = None
        if include_audio:
            try:
                audio_response = await elevenlabs_service.generate_audio(
                    text=analysis.patrick_critique, voice_id=voice_id
                )
            except Exception as e:
                # Don't fail the entire request if audio generation fails
                print(f"Audio generation failed: {str(e)}")

        processing_time = time.time() - start_time

        return AnalysisResponse(
            id=analysis_id,
            analysis=analysis,
            audio=audio_response,
            processing_time=processing_time,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post(
    "/image-only",
    response_model=BusinessCardAnalysis,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def analyze_business_card_image_only(file: UploadFile = File(...)):
    """
    Image analysis only - no audio generation
    """
    try:
        # Validate image
        image_processor.validate_image(file)

        # Analyze business card with Gemini
        analysis = await gemini_service.analyze_business_card(file)

        return analysis

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Psycho Score Analysis API"}
