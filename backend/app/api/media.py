"""
KalaiPaalam AI - Media Upload & Processing Endpoints
Provides standalone AI Studio image enhancement and Bhashini voice transcription.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.services.image_service import image_service
from app.services.voice_service import speech_service

router = APIRouter(prefix="/api/media", tags=["Media"])

@router.post("/process_image")
async def process_image(image: UploadFile = File(...)):
    """
    Stand-alone AI Studio test:
    Executes OpenCV GrabCut edge matting, lighting normalization, and catalog canvas composition.
    """
    content = await image.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty image file")
    
    result = image_service.process_craft_image(content, image.filename)
    return {
        "success": True,
        "image_data": result
    }

@router.post("/process_voice")
async def process_voice(
    voice: Optional[UploadFile] = File(None),
    spoken_text: Optional[str] = Form(None),
    language: str = Form("ta")
):
    """
    Stand-alone Bhashini Speech & Translation test:
    Transcribes audio or test speech and outputs English + Hindi translations.
    """
    audio_bytes = await voice.read() if voice else None
    result = speech_service.transcribe_and_translate(
        audio_data=audio_bytes,
        spoken_text=spoken_text,
        source_lang=language
    )
    return {
        "success": True,
        "speech_data": result
    }
