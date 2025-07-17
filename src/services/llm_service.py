import os
import json
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://nirogai.com',
            'X-Title': 'NirogAI Medical Assistant'
        }
        
        # Disease-specific system prompts
        self.disease_prompts = {
            "fever": """You are a medical AI assistant specializing in fever-related conditions. 
            Analyze the symptoms and provide concise, helpful information about possible causes 
            and general care recommendations. Focus on fever management, hydration, and when to seek medical care.
            Always include a medical disclaimer that this is not professional medical advice.""",
            
            "respiratory": """You are a medical AI assistant specializing in respiratory conditions.
            Focus on cough, breathing difficulties, chest pain, and lung-related symptoms. 
            Provide guidance on respiratory care, when symptoms are concerning, and general management.
            Always include a medical disclaimer that this is not professional medical advice.""",
            
            "digestive": """You are a medical AI assistant specializing in digestive and gastrointestinal conditions.
            Focus on stomach pain, nausea, vomiting, diarrhea, and digestive issues.
            Provide guidance on dietary management and when to seek medical care.
            Always include a medical disclaimer that this is not professional medical advice.""",
            
            "neurological": """You are a medical AI assistant specializing in neurological symptoms.
            Focus on headaches, dizziness, confusion, and nervous system related symptoms.
            Provide guidance on symptom management and when immediate medical attention is needed.
            Always include a medical disclaimer that this is not professional medical advice.""",
            
            "cardiovascular": """You are a medical AI assistant specializing in cardiovascular conditions.
            Focus on chest pain, heart palpitations, shortness of breath, and circulation issues.
            Emphasize when immediate medical attention is required for heart-related symptoms.
            Always include a medical disclaimer that this is not professional medical advice.""",
            
            "musculoskeletal": """You are a medical AI assistant specializing in musculoskeletal conditions.
            Focus on joint pain, muscle aches, bone pain, and mobility issues.
            Provide guidance on pain management, rest, and when to seek medical evaluation.
            Always include a medical disclaimer that this is not professional medical advice.""",
            
            "general": """You are a medical AI assistant providing general health guidance.
            Analyze the described symptoms and provide helpful, concise information about possible causes
            and general care recommendations. Focus on symptom management and when to seek professional care.
            Always include a medical disclaimer that this is not professional medical advice."""
        }
        
        # Language-specific instructions
        self.language_instructions = {
            "en": "Respond in clear, simple English.",
            "hi": "Respond in Hindi (हिंदी). Use simple, clear language that is easy to understand.",
            "ta": "Respond in Tamil (தமிழ்). Use simple, clear language that is easy to understand.",
            "bn": "Respond in Bengali (বাংলা). Use simple, clear language that is easy to understand.",
            "te": "Respond in Telugu (తెలుగు). Use simple, clear language that is easy to understand.",
            "mr": "Respond in Marathi (मराठी). Use simple, clear language that is easy to understand.",
            "gu": "Respond in Gujarati (ગુજરાતી). Use simple, clear language that is easy to understand.",
            "kn": "Respond in Kannada (ಕನ್ನಡ). Use simple, clear language that is easy to understand."
        }

    def detect_condition_category(self, symptoms: str) -> str:
        """Detect the primary condition category from symptoms"""
        symptoms_lower = symptoms.lower()
        
        # Fever-related keywords
        fever_keywords = ['fever', 'temperature', 'hot', 'chills', 'sweating', 'बुखार', 'காய்ச்சல்', 'জ্বর']
        if any(keyword in symptoms_lower for keyword in fever_keywords):
            return "fever"
        
        # Respiratory keywords
        respiratory_keywords = ['cough', 'breathing', 'chest', 'lungs', 'shortness of breath', 'wheeze', 'खांसी', 'இருமல்', 'কাশি']
        if any(keyword in symptoms_lower for keyword in respiratory_keywords):
            return "respiratory"
        
        # Digestive keywords
        digestive_keywords = ['stomach', 'nausea', 'vomiting', 'diarrhea', 'abdominal', 'digestion', 'पेट', 'வயிறு', 'পেট']
        if any(keyword in symptoms_lower for keyword in digestive_keywords):
            return "digestive"
        
        # Neurological keywords
        neuro_keywords = ['headache', 'dizziness', 'confusion', 'memory', 'सिरदर्द', 'தலைவலி', 'মাথাব্যথা']
        if any(keyword in symptoms_lower for keyword in neuro_keywords):
            return "neurological"
        
        # Cardiovascular keywords
        cardio_keywords = ['heart', 'chest pain', 'palpitations', 'circulation', 'दिल', 'இதயம்', 'হৃদয়']
        if any(keyword in symptoms_lower for keyword in cardio_keywords):
            return "cardiovascular"
        
        # Musculoskeletal keywords
        musculo_keywords = ['joint', 'muscle', 'bone', 'pain', 'ache', 'जोड़', 'மூட்டு', 'জয়েন্ট']
        if any(keyword in symptoms_lower for keyword in musculo_keywords):
            return "musculoskeletal"
        
        return "general"

    def analyze_symptoms(self, symptoms: str, language: str = "en") -> Dict:
        """Analyze symptoms using OpenRouter LLM"""
        try:
            # Detect condition category
            condition_category = self.detect_condition_category(symptoms)
            
            # Get appropriate system prompt
            system_prompt = self.disease_prompts.get(condition_category, self.disease_prompts["general"])
            
            # Add language instruction
            language_instruction = self.language_instructions.get(language, self.language_instructions["en"])
            
            # Construct the full prompt
            full_prompt = f"{system_prompt}\n\n{language_instruction}\n\nProvide a concise response (maximum 200 words) that includes:\n1. Possible causes\n2. General recommendations\n3. When to seek medical care\n4. Medical disclaimer"
            
            # Prepare the request
            payload = {
                "model": "anthropic/claude-3.5-sonnet",  # Using Claude for medical analysis
                "messages": [
                    {
                        "role": "system",
                        "content": full_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Symptoms: {symptoms}"
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.3,  # Lower temperature for more consistent medical advice
                "top_p": 0.9
            }
            
            # Make the API request
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result['choices'][0]['message']['content']
                
                return {
                    "success": True,
                    "analysis": analysis,
                    "condition_category": condition_category,
                    "language": language,
                    "model_used": "anthropic/claude-3.5-sonnet"
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed with status {response.status_code}",
                    "details": response.text
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout - please try again"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }

    def get_health_info(self, topic: str, language: str = "en") -> Dict:
        """Get detailed health information about a specific topic"""
        try:
            language_instruction = self.language_instructions.get(language, self.language_instructions["en"])
            
            system_prompt = f"""You are a medical information assistant. Provide comprehensive, accurate health information about the requested topic.
            {language_instruction}
            
            Structure your response with:
            1. Overview of the condition
            2. Common symptoms
            3. Causes
            4. Treatment options
            5. Prevention tips
            6. When to seek medical care
            
            Keep the response informative but accessible to general audiences."""
            
            payload = {
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Provide detailed health information about: {topic}"
                    }
                ],
                "max_tokens": 800,
                "temperature": 0.2,
                "top_p": 0.9
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                return {
                    "success": True,
                    "content": content,
                    "topic": topic,
                    "language": language
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed with status {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating health information: {str(e)}"
            }

# Create a global instance
llm_service = LLMService()

