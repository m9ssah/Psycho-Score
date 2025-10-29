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

        # Step 3: Take Patrick's description and send to ElevenLabs with your custom voice
        audio_response = await elevenlabs_service.generate_audio(
            text=analysis.patrick_critique,
            voice_id=None,  # This will use your custom voice from settings
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


@router.post("/alpha-vs-beta")
async def alpha_vs_beta_battle(
    original: UploadFile = File(..., description="The original business card"),
    contender: UploadFile = File(..., description="The contender's business card"),
):
    """
    🥊 ALPHA VS BETA BATTLE - Patrick Bateman decides who dominates!

    Upload two business cards for a competitive analysis:
    1. Original card (your baseline)
    2. Contender card (the challenger)

    Patrick will analyze both and declare one as ALPHA (superior) or BETA (inferior)
    with a dramatic audio announcement of the verdict!
    """
    try:
        # Step 1: Validate both uploaded images
        image_processor.validate_image(original)
        image_processor.validate_image(contender)

        # Step 2: Send both cards to Gemini for competitive analysis
        comparison = await gemini_service.compare_business_cards(original, contender)

        # Step 3: Determine the verdict and create announcement
        verdict = comparison.get("final_verdict", "BETA")
        winner_reasoning = comparison.get(
            "winner_reasoning", "Superior design execution"
        )

        # Create dramatic announcement text
        if verdict == "ALPHA":
            announcement_text = f"ALPHA! The challenger card dominates with superior sophistication. {winner_reasoning}"
        else:
            announcement_text = f"BETA! The challenger card has been defeated by inferior execution. {winner_reasoning}"

        # Step 4: Generate audio announcement with your custom voice
        audio_response = await elevenlabs_service.generate_audio(
            text=announcement_text,
            voice_id=None,  # Uses your custom voice from settings
        )

        # Step 5: Return complete battle results
        return {
            "battle_result": {
                "verdict": verdict,
                "winner": "original" if verdict == "ALPHA" else "contender",
                "announcement": announcement_text,
                "audio_url": audio_response.audio_url,
            },
            "detailed_analysis": {
                "original_card": comparison.get("card1_analysis", {}),
                "contender_card": comparison.get("card2_analysis", {}),
                "patrick_comparison": comparison.get("comparison_critique", ""),
                "winner_reasoning": winner_reasoning,
            },
            "scores": {
                "original_score": comparison.get("card1_analysis", {}).get(
                    "psycho_score", 0
                ),
                "contender_score": comparison.get("card2_analysis", {}).get(
                    "psycho_score", 0
                ),
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Battle analysis error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Psycho Score API"}
