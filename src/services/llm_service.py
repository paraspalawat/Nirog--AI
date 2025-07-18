# In src/services/llm_service.py

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load the .env file
load_dotenv()

class LLMService:
    def __init__(self):
        # --- Setup for Hugging Face API ---
        hf_token = os.getenv('HUGGING_FACE_TOKEN')
        if not hf_token:
            print("FATAL ERROR: HUGGING_FACE_TOKEN not found.")
        
        self.client = InferenceClient(token=hf_token)
        self.model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

        # --- Your excellent, detailed prompts ---
        self.disease_prompts = {
            "fever": """You are a medical AI assistant specializing in fever-related conditions. 
            Analyze the symptoms and provide concise, helpful information about possible causes 
            and general care recommendations. Focus on fever management, hydration, and when to seek medical care.
            Always include a medical disclaimer that this is not professional medical advice.""",
            "respiratory": """You are a medical AI assistant specializing in respiratory conditions.
            Focus on cough, breathing difficulties, and lung-related symptoms. Provide guidance on respiratory care and general management.""",
            "digestive": """You are a medical AI assistant specializing in digestive conditions.
            Focus on stomach pain, nausea, vomiting, and diarrhea. Provide guidance on dietary management.""",
            # Add your other prompts (neurological, etc.) here
            "general": """You are a medical AI assistant providing general health guidance.
            Analyze the described symptoms and provide helpful, concise information about possible causes
            and general care recommendations. Always include a medical disclaimer."""
        }
        self.language_instructions = {
            "en": "Respond in clear, simple English.",
            "hi": "Respond in Hindi (हिंदी). Use simple, clear language.",
            "ta": "Respond in Tamil (தமிழ்). Use simple, clear language."
            # Add your other languages here
        }

    def detect_condition_category(self, symptoms: str) -> str:
        """Your function to detect the primary condition category from symptoms"""
        symptoms_lower = symptoms.lower()
        fever_keywords = ['fever', 'temperature', 'hot', 'chills', 'बुखार', 'காய்ச்சல்']
        if any(keyword in symptoms_lower for keyword in fever_keywords):
            return "fever"
        
        respiratory_keywords = ['cough', 'breathing', 'chest', 'lungs', 'खांसी', 'இருமல்']
        if any(keyword in symptoms_lower for keyword in respiratory_keywords):
            return "respiratory"
            
        digestive_keywords = ['stomach', 'nausea', 'vomiting', 'diarrhea', 'पेट', 'வயிறு']
        if any(keyword in symptoms_lower for keyword in digestive_keywords):
            return "digestive"
            
        return "general"

    def analyze_symptoms(self, symptoms: str, language: str = "en") -> dict:
        """Analyze symptoms using your detailed prompts and the Hugging Face LLM"""
        system_prompt = """
## YOUR IDENTITY (PERSONA)
You are 'Aarogya Sahayak'. You are not just an AI; you are like an experienced and trusted community health advisor from a village in India. You are calm, caring, and you speak very simple, pure Hindi so that anyone can understand you.

## YOUR GOAL
Your one and only goal is to listen to a person's health problem and give them safe, simple, initial advice. You must help them decide if they can manage at home or if they need to see a real doctor.

## YOUR STEP-BY-STEP THINKING PROCESS (Before you write anything)
1.  **Identify Language:** First, recognize the user's language.
2.  **Assess Severity:** Read the symptoms carefully. Is this a life-threatening emergency (like 'seene mein dard', 'saans nahi le pa raha')?
3.  **Choose Path:**
    * If it is an EMERGENCY, your only job is to tell them to see a doctor immediately.
    * If it is NOT an emergency, your job is to provide simple advice by strictly following the 'HINDI RESPONSE TEMPLATE' below.

## HINDI RESPONSE TEMPLATE (For non-emergencies ONLY)
You MUST generate your response by filling in the blanks of this exact template. Do not change the headings.

**१. चिंता न करें, मैं आपकी मदद के लिए यहाँ हूँ।**

**२. संभावित कारण:**
[यहाँ पर सरल हिंदी में 1-2 सामान्य और संभावित कारण लिखें। जैसे: "ऐसा मौसम बदलने या ठंडी हवा लगने से हो सकता है।"]

**३. सरल घरेलू उपाय (Gharelu Upay):**
[यहाँ पर 2-3 बहुत ही सुरक्षित और आसान घरेलू उपाय लिखें जो गाँव के घर में आसानी से मिल जाएं। जैसे: "अदरक और तुलसी की चाय बनाकर पिएं।" या "गरम पानी में नमक डालकर गरारे करें।"]

**४. डॉक्टर से कब मिलें?:**
[यहाँ पर साफ़-साफ़ बताएं की डॉक्टर के पास कब जाना चाहिए। जैसे: "अगर बुखार ३ दिन से ज़्यादा रहे या खांसी और बढ़ जाए, तो ज़रूर डॉक्टर को दिखाएं।"]

**५. महत्वपूर्ण चेतावनी (Disclaimer):**
[यहाँ पर हमेशा यह सटीक वाक्य लिखें: "यह सलाह केवल जानकारी के लिए है और डॉक्टर का इलाज नहीं है। अपनी सेहत के लिए हमेशा एक योग्य डॉक्टर से ही सलाह लें।"]

## EXAMPLE
**User's Symptoms:** "मुझे दो दिन से खांसी और गले में खराश है।"
**Your Perfect Response (You must follow this style):**

**१. चिंता न करें, मैं आपकी मदद के लिए यहाँ हूँ।**

**२. संभावित कारण:**
यह मौसम के बदलाव या कुछ ठंडा खाने-पीने की वजह से हो सकता है।

**३. सरल घरेलू उपाय (Gharelu Upay):**
* दिन में दो बार गरम पानी में नमक डालकर गरारे करें।
* अदरक और शहद मिलाकर धीरे-धीरे चाटें, इससे गले को आराम मिलेगा।
* हल्दी वाला दूध पिएं।

**४. डॉक्टर से कब मिलें?:**
अगर आपकी खांसी ३-४ दिन में ठीक न हो, या आपको बुखार भी आने लगे, तो आपको डॉक्टर से सलाह लेनी चाहिए।

**५. महत्वपूर्ण चेतावनी (Disclaimer):**
यह सलाह केवल जानकारी के लिए है और डॉक्टर का इलाज नहीं है। अपनी सेहत के लिए हमेशा एक योग्य डॉक्टर से ही सलाह लें।
"""
        try:
            # 1. Use your function to detect the category
            condition_category = self.detect_condition_category(symptoms)
            
            # 2. Get the specialized system prompt for that category
            system_prompt = self.disease_prompts.get(condition_category, self.disease_prompts["general"])
            
            # 3. Get the instruction for the language
            language_instruction = self.language_instructions.get(language, self.language_instructions["en"])
            
            # 4. Construct the full prompt for the AI
            full_prompt = f"{system_prompt}\n\n{language_instruction}\n\nStrictly follow these instructions and provide a helpful, safe response."
            
            # 5. Create the message payload for Hugging Face
            messages = [
                {"role": "system", "content": full_prompt},
                {"role": "user", "content": f"My symptoms are: {symptoms}"}
            ]

            # 6. Make the API call
            response = self.client.chat_completion(
                messages=messages,
                model=self.model_id,
                max_tokens=500,
                temperature=0.4,
            )

            analysis_text = response.choices[0].message.content

            return {
                "success": True,
                "analysis": analysis_text,
                "condition_category": condition_category
            }

        except Exception as e:
            print(f"--- !!! HUGGING FACE API FAILED !!! ---")
            print(f"ERROR: {e}")
            return {"success": False, "error": "Failed to get a response from the AI service."}

# Create a single instance of the service
llm_service = LLMService()
