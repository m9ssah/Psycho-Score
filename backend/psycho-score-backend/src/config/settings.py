import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # API keys and configuration
    GEMINI_API_KEY: str
    ELEVENLABS_API_KEY: str

    # File paths
    IMAGE_UPLOAD_PATH: str = "uploads/images"
    AUDIO_OUTPUT_PATH: str = "outputs/audio"

    # ElevenLabs configuration
    ELEVENLABS_BASE_URL: str = "https://api.elevenlabs.io/v1"
    PATRICK_VOICE_ID: str = (
        "pNInz6obpgDQGcFmaJgB"  # Default voice ID for Patrick Bateman-like voice
    )

    # Application settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/jpg"]

    class Config:
        env_file = ".env"


settings = Settings()

# Create necessary directories
os.makedirs(settings.IMAGE_UPLOAD_PATH, exist_ok=True)
os.makedirs(settings.AUDIO_OUTPUT_PATH, exist_ok=True)
