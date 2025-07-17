from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
import logging
from datetime import datetime
from src.services.speech_service import speech_service

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

speech_bp = Blueprint('speech', __name__)

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.ogg', '.flac'}

@speech_bp.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech audio to text"""
    try:
        # Check if file is present in request
        if 'audio' not in request.files:
            return jsonify({
                "success": False,
                "error": "No audio file provided"
            }), 400
        
        file = request.files['audio']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400
        
        # Get language parameter
        language = request.form.get('language', 'en')
        
        # Validate language
        supported_languages = ['en', 'hi', 'ta', 'bn', 'te', 'mr', 'gu', 'kn']
        if language not in supported_languages:
            language = 'en'  # Default to English
        
        # Validate file
        if not _allowed_file(file.filename):
            return jsonify({
                "success": False,
                "error": f"Unsupported file format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, f"temp_audio_{datetime.utcnow().timestamp()}_{filename}")
        
        try:
            file.save(temp_path)
            
            # Validate the saved file
            validation_result = speech_service.validate_audio_file(temp_path)
            if not validation_result.get('valid', False):
                return jsonify({
                    "success": False,
                    "error": validation_result.get('error', 'Invalid audio file')
                }), 400
            
            # Log the request
            logger.info(f"Processing speech-to-text for language: {language}, file: {filename}")
            
            # Transcribe the audio
            transcription_result = speech_service.transcribe_audio(temp_path, language)
            
            # Prepare response
            if transcription_result.get('success', False):
                response_data = {
                    "success": True,
                    "data": {
                        "text": transcription_result['text'],
                        "confidence": transcription_result.get('confidence', 0.0),
                        "language": language,
                        "method": transcription_result.get('method', 'unknown'),
                        "file_info": {
                            "filename": filename,
                            "size": validation_result.get('file_size', 0),
                            "format": validation_result.get('format', 'unknown')
                        }
                    },
                    "timestamp": datetime.utcnow().isoformat(),
                    "request_id": f"speech_{datetime.utcnow().timestamp()}"
                }
                
                return jsonify(response_data), 200
            else:
                return jsonify({
                    "success": False,
                    "error": transcription_result.get('error', 'Transcription failed'),
                    "details": transcription_result
                }), 500
                
        finally:
            # Clean up temporary file
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {temp_path}: {e}")
        
    except Exception as e:
        logger.error(f"Error in speech_to_text: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "details": str(e) if request.args.get('debug') else None
        }), 500

@speech_bp.route('/speech/supported-formats', methods=['GET'])
def get_supported_formats():
    """Get list of supported audio formats"""
    try:
        return jsonify({
            "success": True,
            "data": {
                "supported_formats": list(ALLOWED_EXTENSIONS),
                "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024),
                "supported_languages": [
                    {
                        "code": "en",
                        "name": "English",
                        "recognition_code": "en-US"
                    },
                    {
                        "code": "hi",
                        "name": "Hindi",
                        "recognition_code": "hi-IN"
                    },
                    {
                        "code": "ta",
                        "name": "Tamil",
                        "recognition_code": "ta-IN"
                    },
                    {
                        "code": "bn",
                        "name": "Bengali",
                        "recognition_code": "bn-IN"
                    },
                    {
                        "code": "te",
                        "name": "Telugu",
                        "recognition_code": "te-IN"
                    },
                    {
                        "code": "mr",
                        "name": "Marathi",
                        "recognition_code": "mr-IN"
                    },
                    {
                        "code": "gu",
                        "name": "Gujarati",
                        "recognition_code": "gu-IN"
                    },
                    {
                        "code": "kn",
                        "name": "Kannada",
                        "recognition_code": "kn-IN"
                    }
                ]
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_supported_formats: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@speech_bp.route('/speech/test', methods=['GET'])
def test_speech_service():
    """Test endpoint to check if speech service is working"""
    try:
        return jsonify({
            "success": True,
            "message": "Speech service is operational",
            "service_info": {
                "speech_recognition_available": True,
                "supported_formats": list(ALLOWED_EXTENSIONS),
                "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024)
            },
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in test_speech_service: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Speech service test failed",
            "details": str(e)
        }), 500

def _allowed_file(filename):
    """Check if file extension is allowed"""
    if not filename:
        return False
    
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in ALLOWED_EXTENSIONS

