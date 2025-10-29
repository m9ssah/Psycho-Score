from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class BusinessCard(BaseModel):
    image_url: str
    description: Optional[str] = None


class BusinessCardAnalysis(BaseModel):
    """Schema for business card analysis results"""

    card_quality: str = Field(..., description="Overall quality assessment")
    design_elements: Dict[str, Any] = Field(..., description="Design analysis")
    typography: Dict[str, Any] = Field(..., description="Font and typography analysis")
    color_scheme: Dict[str, Any] = Field(..., description="Color analysis")
    layout_quality: str = Field(..., description="Layout assessment")
    material_impression: str = Field(..., description="Perceived material quality")
    patrick_critique: str = Field(..., description="Patrick Bateman style critique")
    psycho_score: float = Field(..., ge=0, le=10, description="Final score out of 10")


class AnalysisResult(BaseModel):
    name: str
    title: str
    company: str
    email: str
    phone: str
    description: str


class AudioResponse(BaseModel):
    """Schema for audio generation response"""

    audio_url: str = Field(..., description="URL to generated audio file")
    audio_duration: Optional[float] = Field(None, description="Duration in seconds")
    file_size: Optional[int] = Field(None, description="File size in bytes")


class AnalysisRequest(BaseModel):
    """Schema for analysis request"""

    include_audio: bool = Field(default=True, description="Whether to generate audio")
    voice_id: Optional[str] = Field(None, description="ElevenLabs voice ID override")


class AnalysisResponse(BaseModel):
    """Schema for complete analysis response"""

    id: str = Field(..., description="Unique analysis ID")
    analysis: BusinessCardAnalysis
    audio: Optional[AudioResponse] = None
    created_at: datetime = Field(default_factory=datetime.now)
    processing_time: float = Field(..., description="Processing time in seconds")


class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "Patrick Bateman"  # Default voice style


class TTSResponse(BaseModel):
    audio_url: str
    message: str


class ErrorResponse(BaseModel):
    """Schema for error responses"""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    error_code: Optional[str] = Field(None, description="Error code")
