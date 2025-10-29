from fastapi import APIRouter, File, UploadFile, HTTPException
from services.gemini_service import gemini_service
from services.elevenlabs_service import elevenlabs_service
from utils.image_processing import image_processor

router = APIRouter()


@router.post("/psycho-score")
async def psycho_score_analysis(file: UploadFile = File(...)):
    """
    🎭 PSYCHO SCORE - The main endpoint that does exactly what you described:

    1. User uploads business card image
    2. Gemini analyzes shape, color, font, and details
    3. Generates Patrick Bateman-style description
    4. Sends to ElevenLabs for TTS in Patrick's voice
    5. Returns complete result to user
    """
    try:
        # Step 1: Validate uploaded business card image
        image_processor.validate_image(file)

        # Step 2: Send to Gemini for analysis (shape, color, font, details)
        analysis = await gemini_service.analyze_business_card(file)

        # Step 3: Take Patrick's description and send to ElevenLabs
        audio_response = await elevenlabs_service.generate_audio(
            text=analysis.patrick_critique
        )

        # Step 4: Return complete result to user
        return {
            "psycho_score": analysis.psycho_score,
            "patrick_critique": analysis.patrick_critique,
            "audio_url": audio_response.audio_url,
            "analysis_details": {
                "typography": analysis.typography,
                "color_scheme": analysis.color_scheme,
                "design_elements": analysis.design_elements,
                "material_impression": analysis.material_impression,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/quick-analysis")
async def quick_business_card_analysis(file: UploadFile = File(...)):
    """
    Quick analysis without audio - just Patrick's written critique
    """
    try:
        image_processor.validate_image(file)
        analysis = await gemini_service.analyze_business_card(file)

        return {
            "psycho_score": analysis.psycho_score,
            "patrick_critique": analysis.patrick_critique,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Psycho Score API"}
