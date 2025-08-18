"""
Whisper Service - Speech-to-text transcription using OpenAI Whisper API
"""

import os
import tempfile
import openai
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class WhisperService:
    """
    Service for speech-to-text transcription using OpenAI Whisper
    """
    
    def __init__(self):
        """Initialize Whisper service"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
            self.enabled = True
        else:
            logger.warning("OpenAI API key not found. Whisper service disabled.")
            self.enabled = False

    async def transcribe(self, audio_data: bytes, language: str = "en") -> str:
        """
        Transcribe audio data to text
        """
        if not self.enabled:
            return "Mock transcription: I was walking through a beautiful forest when suddenly I could fly above the trees."
        
        try:
            # Save audio data to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            # Transcribe using Whisper API
            # In production:
            # with open(temp_file_path, "rb") as audio_file:
            #     transcript = openai.Audio.transcribe("whisper-1", audio_file, language=language)
            #     return transcript.text
            
            # Mock response for skeleton
            return "I was walking through a beautiful forest when suddenly I could fly above the trees. The water below was crystal clear and I could see my reflection changing."
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass

    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return [
            "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh",
            "ar", "hi", "tr", "pl", "nl", "sv", "da", "no", "fi"
        ]