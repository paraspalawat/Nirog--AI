# NirogAI Backend - Medical Chatbot with LLM Integration

A Python Flask backend for NirogAI medical chatbot that provides disease-specific symptom analysis using OpenRouter LLM API, with speech recognition support and multilingual capabilities.

## Features

- 🤖 **AI-Powered Symptom Analysis**: Uses Claude 3.5 Sonnet via OpenRouter for medical insights
- 🌍 **Multilingual Support**: 8 Indian languages (English, Hindi, Tamil, Bengali, Telugu, Marathi, Gujarati, Kannada)
- 🎤 **Speech Recognition**: Convert speech to text for accessibility
- 🏥 **Disease-Specific Responses**: Different AI responses based on detected medical conditions
- 📱 **Responsive Frontend**: Mobile-friendly web interface
- 🔒 **Secure**: Proper input validation and medical disclaimers

## Supported Languages

- English (en)
- हिंदी - Hindi (hi)
- தமிழ் - Tamil (ta)
- বাংলা - Bengali (bn)
- తెలుగు - Telugu (te)
- मराठी - Marathi (mr)
- ગુજરાતી - Gujarati (gu)
- ಕನ್ನಡ - Kannada (kn)

## API Endpoints

### Symptom Analysis
```
POST /api/analyze-symptoms
Content-Type: application/json

{
    "symptoms": "I have headache and fever for 2 days",
    "language": "en",
    "user_id": "optional_user_id"
}
```

### Speech Recognition
```
POST /api/speech-to-text
Content-Type: multipart/form-data

Form Data:
- audio: audio file (wav, mp3, m4a, ogg, flac)
- language: language code
```

### Health Information
```
GET /api/health-info/{topic}?lang={language_code}
```

### Supported Languages
```
GET /api/languages
```

## Installation & Setup

### Prerequisites
- Python 3.11+
- Virtual environment support
- Internet connection for LLM API calls

### 1. Clone and Setup
```bash
# The project is already set up in /home/ubuntu/nirogai-backend
cd /home/ubuntu/nirogai-backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies (already done)
pip install -r requirements.txt
```

### 2. Environment Configuration
Create `.env` file with your OpenRouter API key:
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

### 3. Run Development Server
```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
python src/main.py
```

The application will be available at:
- Local: http://127.0.0.1:5000
- Network: http://0.0.0.0:5000

## Project Structure

```
nirogai-backend/
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── test_results.md          # Test documentation
├── venv/                    # Virtual environment
└── src/
    ├── main.py              # Flask application entry point
    ├── static/              # Frontend files (HTML, CSS, JS)
    │   ├── index.html
    │   ├── styles.css
    │   └── script.js
    ├── routes/              # API route handlers
    │   ├── symptoms.py      # Symptom analysis endpoints
    │   ├── speech.py        # Speech recognition endpoints
    │   └── user.py          # User management (template)
    ├── services/            # Business logic services
    │   ├── llm_service.py   # OpenRouter LLM integration
    │   └── speech_service.py # Speech recognition service
    ├── models/              # Database models (if needed)
    └── database/            # SQLite database files
```

## Dependencies

### Core Dependencies
- **Flask**: Web framework
- **flask-cors**: Cross-origin resource sharing
- **python-dotenv**: Environment variable management
- **requests**: HTTP client for API calls

### AI/ML Dependencies
- **openai**: OpenAI-compatible client for OpenRouter
- **SpeechRecognition**: Speech-to-text functionality
- **pydub**: Audio file processing

### Full Requirements
```
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certifi==2025.7.14
charset-normalizer==3.4.2
click==8.2.1
distro==1.9.0
Flask==3.1.1
flask-cors==6.0.0
Flask-SQLAlchemy==3.1.1
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
MarkupSafe==3.0.2
openai==1.97.0
pydantic==2.11.7
pydantic-core==2.33.2
pydub==0.25.1
python-dotenv==1.1.1
requests==2.32.4
sniffio==1.3.1
SpeechRecognition==3.14.3
SQLAlchemy==2.0.41
tqdm==4.67.1
typing-extensions==4.14.0
typing-inspection==0.4.1
urllib3==2.5.0
Werkzeug==3.1.3
```

## Deployment Options

### Option 1: Local Development
```bash
# Already running on localhost:5000
source venv/bin/activate
python src/main.py
```

### Option 2: Production with Gunicorn
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

### Option 3: Using Manus Deployment Service
```bash
# Deploy to public internet (if available)
# This would make the app accessible via a public URL
```

## Configuration

### OpenRouter API Setup
1. Sign up at [OpenRouter](https://openrouter.ai/)
2. Get your API key
3. Add it to the `.env` file
4. The app uses Claude 3.5 Sonnet model for medical analysis

### Speech Recognition Setup
- Uses Google Speech Recognition API (free tier)
- Fallback to offline Sphinx for English
- Supports multiple audio formats

## Usage Examples

### 1. Symptom Analysis
```javascript
// Frontend JavaScript example
const response = await fetch('/api/analyze-symptoms', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        symptoms: "I have fever and headache",
        language: "en"
    })
});
const result = await response.json();
```

### 2. Speech Recognition
```javascript
// Upload audio file for transcription
const formData = new FormData();
formData.append('audio', audioFile);
formData.append('language', 'en');

const response = await fetch('/api/speech-to-text', {
    method: 'POST',
    body: formData
});
```

## Medical Disclaimer

⚠️ **Important**: This application provides AI-generated health information for educational purposes only. It should not replace professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical concerns.

## Security Considerations

- API keys stored in environment variables
- Input validation on all endpoints
- File upload restrictions for speech recognition
- CORS properly configured
- Medical disclaimers included in all responses
- No sensitive medical data stored

## Testing

The application has been tested with:
- ✅ Symptom analysis in English
- ✅ Disease category detection (fever, respiratory, etc.)
- ✅ Frontend-backend integration
- ✅ API response formatting
- ✅ Error handling

See `test_results.md` for detailed test documentation.

## Troubleshooting

### Common Issues

1. **OpenRouter API Errors**
   - Check API key in `.env` file
   - Verify internet connection
   - Check OpenRouter account credits

2. **Speech Recognition Fails**
   - Ensure microphone permissions
   - Check audio file format
   - Verify file size (max 10MB)

3. **CORS Issues**
   - CORS is enabled for all origins
   - Check browser console for errors

4. **Module Import Errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

### Logs
Check Flask console output for detailed error messages and API request logs.

## Contributing

1. Follow the existing code structure
2. Add proper error handling
3. Include medical disclaimers
4. Test with multiple languages
5. Update documentation

## License

This project is for educational and demonstration purposes. Please ensure compliance with medical software regulations in your jurisdiction.

## Support

For technical support or questions about the implementation, please refer to the code comments and documentation.

