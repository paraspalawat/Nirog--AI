from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
from src.services.llm_service import llm_service

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

symptoms_bp = Blueprint('symptoms', __name__)

@symptoms_bp.route('/analyze-symptoms', methods=['POST'])
def analyze_symptoms():
    """Analyze user symptoms and provide AI-powered insights"""
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Validate required fields
        symptoms = data.get('symptoms', '').strip()
        if not symptoms:
            return jsonify({
                "success": False,
                "error": "Symptoms description is required"
            }), 400
        
        # Get optional fields
        language = data.get('language', 'en')
        user_id = data.get('user_id', None)
        
        # Validate language
        supported_languages = ['en', 'hi', 'ta', 'bn', 'te', 'mr', 'gu', 'kn']
        if language not in supported_languages:
            language = 'en'  # Default to English
        
        # Log the request
        logger.info(f"Analyzing symptoms for language: {language}, user: {user_id}")
        
        # Analyze symptoms using LLM service
        analysis_result = llm_service.analyze_symptoms(symptoms, language)
        
        if not analysis_result.get('success', False):
            return jsonify({
                "success": False,
                "error": analysis_result.get('error', 'Analysis failed')
            }), 500
        
        # Prepare response
        response_data = {
            "success": True,
            "data": {
                "analysis": analysis_result['analysis'],
                "condition_category": analysis_result.get('condition_category', 'general'),
                "language": language,
                "severity": _assess_severity(symptoms),
                "recommendations": _get_general_recommendations(language),
                "disclaimer": _get_medical_disclaimer(language)
            },
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": f"req_{datetime.utcnow().timestamp()}"
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_symptoms: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "details": str(e) if request.args.get('debug') else None
        }), 500

@symptoms_bp.route('/health-info/<topic>', methods=['GET'])
def get_health_info(topic):
    """Get detailed health information about a specific topic"""
    try:
        # Get language from query parameters
        language = request.args.get('lang', 'en')
        
        # Validate language
        supported_languages = ['en', 'hi', 'ta', 'bn', 'te', 'mr', 'gu', 'kn']
        if language not in supported_languages:
            language = 'en'
        
        # Get health information using LLM service
        info_result = llm_service.get_health_info(topic, language)
        
        if not info_result.get('success', False):
            return jsonify({
                "success": False,
                "error": info_result.get('error', 'Failed to get health information')
            }), 500
        
        # Prepare response
        response_data = {
            "success": True,
            "data": {
                "topic": topic,
                "title": _get_topic_title(topic, language),
                "content": info_result['content'],
                "language": language
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error in get_health_info: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

@symptoms_bp.route('/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    try:
        languages = [
            {
                "code": "en",
                "name": "English",
                "native_name": "English"
            },
            {
                "code": "hi",
                "name": "Hindi",
                "native_name": "हिंदी"
            },
            {
                "code": "ta",
                "name": "Tamil",
                "native_name": "தமிழ்"
            },
            {
                "code": "bn",
                "name": "Bengali",
                "native_name": "বাংলা"
            },
            {
                "code": "te",
                "name": "Telugu",
                "native_name": "తెలుగు"
            },
            {
                "code": "mr",
                "name": "Marathi",
                "native_name": "मराठी"
            },
            {
                "code": "gu",
                "name": "Gujarati",
                "native_name": "ગુજરાતી"
            },
            {
                "code": "kn",
                "name": "Kannada",
                "native_name": "ಕನ್ನಡ"
            }
        ]
        
        return jsonify({
            "success": True,
            "data": {
                "supported_languages": languages
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_supported_languages: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500

def _assess_severity(symptoms: str) -> str:
    """Assess symptom severity based on keywords"""
    symptoms_lower = symptoms.lower()
    
    # High severity keywords
    high_severity = [
        'severe', 'intense', 'unbearable', 'emergency', 'chest pain', 
        'difficulty breathing', 'unconscious', 'bleeding', 'stroke',
        'heart attack', 'suicide', 'overdose'
    ]
    
    # Medium severity keywords
    medium_severity = [
        'moderate', 'persistent', 'worsening', 'fever', 'vomiting',
        'diarrhea', 'headache', 'pain'
    ]
    
    if any(keyword in symptoms_lower for keyword in high_severity):
        return "high"
    elif any(keyword in symptoms_lower for keyword in medium_severity):
        return "medium"
    else:
        return "low"

def _get_general_recommendations(language: str) -> list:
    """Get general health recommendations based on language"""
    recommendations = {
        "en": [
            "Stay hydrated by drinking plenty of water",
            "Get adequate rest and sleep",
            "Monitor your symptoms closely",
            "Consult a healthcare professional if symptoms persist or worsen",
            "Maintain good hygiene practices"
        ],
        "hi": [
            "पर्याप्त पानी पीकर हाइड्रेटेड रहें",
            "पर्याप्त आराम और नींद लें",
            "अपने लक्षणों की बारीकी से निगरानी करें",
            "यदि लक्षण बने रहते हैं या बिगड़ते हैं तो स्वास्थ्य पेशेवर से सलाह लें",
            "अच्छी स्वच्छता प्रथाओं को बनाए रखें"
        ]
    }
    
    return recommendations.get(language, recommendations["en"])

def _get_medical_disclaimer(language: str) -> str:
    """Get medical disclaimer based on language"""
    disclaimers = {
        "en": "This is AI-generated information and should not replace professional medical advice. Please consult a qualified healthcare provider for proper diagnosis and treatment.",
        "hi": "यह AI-जनित जानकारी है और इसे पेशेवर चिकित्सा सलाह का विकल्प नहीं माना जाना चाहिए। उचित निदान और उपचार के लिए कृपया एक योग्य स्वास्थ्य सेवा प्रदाता से सलाह लें।"
    }
    
    return disclaimers.get(language, disclaimers["en"])

def _get_topic_title(topic: str, language: str) -> str:
    """Get localized title for health topics"""
    titles = {
        "en": {
            "fever": "Understanding Fever",
            "cough": "Understanding Cough",
            "diabetes": "Managing Diabetes",
            "mental-health": "Mental Health & Wellness",
            "first-aid": "First Aid Basics",
            "nutrition": "Nutrition & Healthy Eating"
        },
        "hi": {
            "fever": "बुखार को समझना",
            "cough": "खांसी को समझना",
            "diabetes": "मधुमेह का प्रबंधन",
            "mental-health": "मानसिक स्वास्थ्य और कल्याण",
            "first-aid": "प्राथमिक चिकित्सा की मूल बातें",
            "nutrition": "पोषण और स्वस्थ भोजन"
        }
    }
    
    lang_titles = titles.get(language, titles["en"])
    return lang_titles.get(topic, topic.replace("-", " ").title())

