import httpx
import aiofiles
import os
import uuid
from typing import Optional
from fastapi import HTTPException
from config.settings import settings
from models.schemas import AudioResponse


class ElevenLabsService:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.base_url = settings.ELEVENLABS_BASE_URL
        self.voice_id = settings.PATRICK_VOICE_ID

    async def generate_audio(
        self, text: str, voice_id: Optional[str] = None
    ) -> AudioResponse:
        """Generate audio from text using ElevenLabs API"""
        try:
            # Use provided voice_id or default Patrick voice
            selected_voice_id = voice_id or self.voice_id

            url = f"{self.base_url}/text-to-speech/{selected_voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key,
            }

            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                    "style": 0.0,
                    "use_speaker_boost": True,
                },
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, json=data, headers=headers, timeout=60.0
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"ElevenLabs API error: {response.text}",
                    )

                # Generate unique filename
                audio_filename = f"psycho_analysis_{uuid.uuid4().hex}.mp3"
                audio_path = os.path.join(settings.AUDIO_OUTPUT_PATH, audio_filename)

                # Save audio file
                async with aiofiles.open(audio_path, "wb") as f:
                    await f.write(response.content)

                # Get file size
                file_size = len(response.content)

                # Create audio URL (this would be served by your static file server)
                audio_url = f"/audio/{audio_filename}"

                return AudioResponse(
                    audio_url=audio_url,
                    audio_duration=None,  # Could be calculated if needed
                    file_size=file_size,
                )

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Request to ElevenLabs failed: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error generating audio: {str(e)}"
            )

    async def get_available_voices(self):
        """Get list of available voices from ElevenLabs"""
        try:
            url = f"{self.base_url}/voices"
            headers = {"Accept": "application/json", "xi-api-key": self.api_key}

            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)

                if response.status_code == 200:
                    return response.json()
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Failed to fetch voices: {response.text}",
                    )

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Request to ElevenLabs failed: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error fetching voices: {str(e)}"
            )


# Create global instance
elevenlabs_service = ElevenLabsService()
