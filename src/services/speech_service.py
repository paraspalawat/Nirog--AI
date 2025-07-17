import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
from typing import Dict, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        # Language mapping for speech recognition
        self.language_codes = {
            "en": "en-US",
            "hi": "hi-IN",
            "ta": "ta-IN",
            "bn": "bn-IN",
            "te": "te-IN",
            "mr": "mr-IN",
            "gu": "gu-IN",
            "kn": "kn-IN"
        }
        
        # Supported audio formats
        self.supported_formats = ['.wav', '.mp3', '.m4a', '.ogg', '.flac']

    def convert_audio_to_wav(self, audio_file_path: str) -> str:
        """Convert audio file to WAV format for speech recognition"""
        try:
            # Get file extension
            file_ext = os.path.splitext(audio_file_path)[1].lower()
            
            if file_ext == '.wav':
                return audio_file_path
            
            # Load audio file
            if file_ext == '.mp3':
                audio = AudioSegment.from_mp3(audio_file_path)
            elif file_ext == '.m4a':
                audio = AudioSegment.from_file(audio_file_path, format="m4a")
            elif file_ext == '.ogg':
                audio = AudioSegment.from_ogg(audio_file_path)
            elif file_ext == '.flac':
                audio = AudioSegment.from_file(audio_file_path, format="flac")
            else:
                raise ValueError(f"Unsupported audio format: {file_ext}")
            
            # Create temporary WAV file
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            audio.export(temp_wav.name, format="wav")
            temp_wav.close()
            
            return temp_wav.name
            
        except Exception as e:
            logger.error(f"Error converting audio to WAV: {str(e)}")
            raise

    def transcribe_audio(self, audio_file_path: str, language: str = "en") -> Dict:
        """Transcribe audio file to text"""
        temp_wav_path = None
        
        try:
            # Convert to WAV if necessary
            temp_wav_path = self.convert_audio_to_wav(audio_file_path)
            
            # Get language code for speech recognition
            lang_code = self.language_codes.get(language, "en-US")
            
            # Load audio file
            with sr.AudioFile(temp_wav_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record the audio
                audio_data = self.recognizer.record(source)
            
            # Try Google Speech Recognition first
            try:
                text = self.recognizer.recognize_google(
                    audio_data, 
                    language=lang_code,
                    show_all=False
                )
                
                return {
                    "success": True,
                    "text": text,
                    "confidence": 0.9,  # Google doesn't provide confidence scores
                    "language": language,
                    "method": "google"
                }
                
            except sr.UnknownValueError:
                return {
                    "success": False,
                    "error": "Could not understand the audio",
                    "text": "",
                    "confidence": 0.0
                }
                
            except sr.RequestError as e:
                # Fallback to offline recognition if available
                logger.warning(f"Google Speech Recognition error: {e}")
                return self._fallback_recognition(audio_data, language)
                
        except Exception as e:
            logger.error(f"Error in speech transcription: {str(e)}")
            return {
                "success": False,
                "error": f"Transcription failed: {str(e)}",
                "text": "",
                "confidence": 0.0
            }
            
        finally:
            # Clean up temporary file
            if temp_wav_path and temp_wav_path != audio_file_path:
                try:
                    os.unlink(temp_wav_path)
                except:
                    pass

    def _fallback_recognition(self, audio_data, language: str) -> Dict:
        """Fallback recognition methods when Google fails"""
        try:
            # Try Sphinx (offline) recognition for English
            if language == "en":
                try:
                    text = self.recognizer.recognize_sphinx(audio_data)
                    return {
                        "success": True,
                        "text": text,
                        "confidence": 0.7,
                        "language": language,
                        "method": "sphinx"
                    }
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    pass
            
            # If all methods fail
            return {
                "success": False,
                "error": "All speech recognition methods failed",
                "text": "",
                "confidence": 0.0
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Fallback recognition failed: {str(e)}",
                "text": "",
                "confidence": 0.0
            }

    def validate_audio_file(self, file_path: str) -> Dict:
        """Validate audio file format and size"""
        try:
            if not os.path.exists(file_path):
                return {
                    "valid": False,
                    "error": "File does not exist"
                }
            
            # Check file size (limit to 10MB)
            file_size = os.path.getsize(file_path)
            if file_size > 10 * 1024 * 1024:  # 10MB
                return {
                    "valid": False,
                    "error": "File size too large (max 10MB)"
                }
            
            # Check file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.supported_formats:
                return {
                    "valid": False,
                    "error": f"Unsupported format. Supported: {', '.join(self.supported_formats)}"
                }
            
            # Try to load the audio file to verify it's valid
            try:
                if file_ext == '.wav':
                    with sr.AudioFile(file_path) as source:
                        pass  # Just check if it can be opened
                else:
                    # For other formats, try to load with pydub
                    AudioSegment.from_file(file_path)
                
                return {
                    "valid": True,
                    "file_size": file_size,
                    "format": file_ext
                }
                
            except Exception as e:
                return {
                    "valid": False,
                    "error": f"Invalid audio file: {str(e)}"
                }
                
        except Exception as e:
            return {
                "valid": False,
                "error": f"File validation error: {str(e)}"
            }

# Create a global instance
speech_service = SpeechService()

