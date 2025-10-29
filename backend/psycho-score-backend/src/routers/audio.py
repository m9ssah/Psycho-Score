from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import FileResponse
from typing import Optional
import os
from services.elevenlabs_service import elevenlabs_service
from config.settings import settings

router = APIRouter()


@router.post("/generate")
async def generate_audio_from_text(
    text: str = Form(..., description="Text to convert to speech"),
    voice_id: Optional[str] = Form(
        default=None, description="ElevenLabs voice ID override"
    ),
):
    """Generate audio from text using ElevenLabs TTS"""
    try:
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        if len(text) > 5000:  # ElevenLabs character limit
            raise HTTPException(
                status_code=400, detail="Text too long. Maximum 5000 characters."
            )

        audio_response = await elevenlabs_service.generate_audio(
            text=text, voice_id=voice_id
        )
        return audio_response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")


@router.post("/patrick-critique")
async def generate_patrick_audio(text: str = Form(...)):
    """Generate Patrick Bateman style audio critique"""
    try:
        # Add Patrick Bateman style flair if not already present
        enhanced_text = text
        if not any(
            phrase in enhanced_text.lower()
            for phrase in ["look at that", "subtle", "tasteful", "elegant"]
        ):
            enhanced_text = f"Look at that subtle off-white coloring... {enhanced_text}"

        audio_response = await elevenlabs_service.generate_audio(text=enhanced_text)
        return audio_response

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating Patrick audio: {str(e)}"
        )


@router.get("/voices")
async def get_available_voices():
    """Get list of available ElevenLabs voices"""
    try:
        voices = await elevenlabs_service.get_available_voices()
        return voices
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching voices: {str(e)}")


@router.get("/file/{filename}")
async def get_audio_file(filename: str):
    """Serve audio files"""
    file_path = os.path.join(settings.AUDIO_OUTPUT_PATH, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(path=file_path, media_type="audio/mpeg", filename=filename)


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Psycho Score Audio API"}
