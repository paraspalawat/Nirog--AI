// Language translations
const translations = {
    en: {
        brand: "NirogAI",
        nav: {
            home: "Home",
            symptoms: "Symptoms Checker",
            health: "Health Info",
            languages: "Languages",
            about: "About",
            contact: "Contact"
        },
        hero: {
            title: "Welcome to NirogAI – Your Local AI Health Companion",
            subtitle: "Get instant health insights in your preferred language with AI-powered assistance",
            cta: "Start Checking"
        },
        symptoms: {
            title: "AI Symptoms Checker",
            subtitle: "Describe your symptoms and get instant AI-powered insights",
            label: "Describe your symptoms",
            placeholder: "e.g., I have a headache and fever for 2 days...",
            language: "Select Language",
            submit: "Get Diagnosis",
            loading: "Analyzing your symptoms...",
            result: {
                title: "AI Analysis Result"
            },
            disclaimer: "This is AI-generated information and should not replace professional medical advice.",
            history: {
                title: "Recent Searches"
            }
        },
        health: {
            title: "Health Information",
            subtitle: "Learn about common health conditions and preventive care",
            fever: {
                title: "Fever",
                desc: "Understanding fever causes and management"
            },
            cough: {
                title: "Cough",
                desc: "Types of cough and treatment options"
            },
            diabetes: {
                title: "Diabetes",
                desc: "Managing diabetes and blood sugar levels"
            },
            mental: {
                title: "Mental Health",
                desc: "Mental wellness and stress management"
            },
            firstaid: {
                title: "First Aid",
                desc: "Emergency first aid procedures"
            },
            nutrition: {
                title: "Nutrition",
                desc: "Healthy eating and dietary guidelines"
            }
        },
        languages: {
            title: "Supported Languages",
            subtitle: "Choose your preferred language for better communication"
        },
        about: {
            title: "About NirogAI",
            desc1: "NirogAI is an innovative AI-powered health assistant designed specifically for India's diverse linguistic landscape. Our mission is to make healthcare information accessible to everyone, regardless of their preferred language.",
            desc2: "With support for multiple Indian languages, NirogAI bridges the gap between advanced AI technology and local healthcare needs, providing instant, reliable health insights in your native language.",
            feature1: "Multi-language Support",
            feature2: "AI-Powered Analysis",
            feature3: "Privacy Protected"
        },
        contact: {
            title: "Contact Us",
            subtitle: "Get in touch with our team for support or feedback",
            email: "Email",
            phone: "Phone",
            address: "Address",
            name: "Your Name",
            "email.placeholder": "Your Email",
            message: "Your Message",
            send: "Send Message"
        },
        footer: {
            desc: "Making healthcare accessible through AI and local languages",
            links: "Quick Links",
            legal: "Legal",
            disclaimer: "Disclaimer",
            privacy: "Privacy Policy",
            terms: "Terms of Service",
            social: "Follow Us"
        }
    },
    hi: {
        brand: "निरोगAI",
        nav: {
            home: "होम",
            symptoms: "लक्षण जांच",
            health: "स्वास्थ्य जानकारी",
            languages: "भाषाएं",
            about: "हमारे बारे में",
            contact: "संपर्क"
        },
        hero: {
            title: "निरोगAI में आपका स्वागत है – आपका स्थानीय AI स्वास्थ्य साथी",
            subtitle: "AI-संचालित सहायता के साथ अपनी पसंदीदा भाषा में तुरंत स्वास्थ्य जानकारी प्राप्त करें",
            cta: "जांच शुरू करें"
        },
        symptoms: {
            title: "AI लक्षण जांच",
            subtitle: "अपने लक्षणों का वर्णन करें और तुरंत AI-संचालित जानकारी प्राप्त करें",
            label: "अपने लक्षणों का वर्णन करें",
            placeholder: "जैसे, मुझे 2 दिनों से सिरदर्द और बुखार है...",
            language: "भाषा चुनें",
            submit: "निदान प्राप्त करें",
            loading: "आपके लक्षणों का विश्लेषण हो रहा है...",
            result: {
                title: "AI विश्लेषण परिणाम"
            },
            disclaimer: "यह AI-जनित जानकारी है और इसे पेशेवर चिकित्सा सलाह का विकल्प नहीं माना जाना चाहिए।",
            history: {
                title: "हाल की खोजें"
            }
        },
        // Add more Hindi translations as needed
    }
    // Add more languages as needed
};

// Global variables
let currentLanguage = 'en';
let searchHistory = JSON.parse(localStorage.getItem('nirogai_history')) || [];
let isRecording = false;
let mediaRecorder = null;
let audioChunks = [];

// API Configuration
const API_BASE_URL = window.location.origin + '/api';

// DOM elements
const navbar = document.getElementById('navbar');
const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');
const symptomsForm = document.getElementById('symptoms-form');
const loadingElement = document.getElementById('loading');
const resultElement = document.getElementById('result');
const historyList = document.getElementById('history-list');
const modal = document.getElementById('health-modal');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set up event listeners
    setupEventListeners();
    
    // Initialize language
    updateLanguage(currentLanguage);
    
    // Load search history
    displaySearchHistory();
    
    // Initialize scroll reveal
    initializeScrollReveal();
    
    // Set up smooth scrolling
    setupSmoothScrolling();
    
    // Add speech recognition button
    addSpeechRecognitionButton();
}

function setupEventListeners() {
    // Navbar toggle
    navToggle.addEventListener('click', toggleNavbar);
    
    // Navbar scroll effect
    window.addEventListener('scroll', handleNavbarScroll);
    
    // Symptoms form
    symptomsForm.addEventListener('submit', handleSymptomsSubmit);
    
    // Contact form
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleContactSubmit);
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeHealthModal();
        }
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', handleKeyboardNavigation);
}

function addSpeechRecognitionButton() {
    // Add speech recognition button to symptoms form
    const symptomsInput = document.getElementById('symptoms-input');
    if (symptomsInput && symptomsInput.parentNode) {
        const speechButton = document.createElement('button');
        speechButton.type = 'button';
        speechButton.className = 'speech-btn';
        speechButton.innerHTML = '<i class="fas fa-microphone"></i>';
        speechButton.title = 'Click to record your symptoms';
        speechButton.onclick = toggleSpeechRecognition;
        
        // Add CSS for speech button
        const style = document.createElement('style');
        style.textContent = `
            .speech-btn {
                position: absolute;
                right: 10px;
                top: 50%;
                transform: translateY(-50%);
                background: var(--primary-blue);
                color: white;
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                cursor: pointer;
                transition: all 0.3s ease;
                z-index: 10;
            }
            .speech-btn:hover {
                background: var(--dark-blue);
                transform: translateY(-50%) scale(1.1);
            }
            .speech-btn.recording {
                background: var(--danger);
                animation: pulse 1s infinite;
            }
            @keyframes pulse {
                0% { transform: translateY(-50%) scale(1); }
                50% { transform: translateY(-50%) scale(1.1); }
                100% { transform: translateY(-50%) scale(1); }
            }
            .form-group {
                position: relative;
            }
        `;
        document.head.appendChild(style);
        
        symptomsInput.parentNode.appendChild(speechButton);
    }
}

async function toggleSpeechRecognition() {
    const speechBtn = document.querySelector('.speech-btn');
    
    if (!isRecording) {
        try {
            // Start recording
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                await processSpeechToText(audioBlob);
                
                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
            };
            
            mediaRecorder.start();
            isRecording = true;
            speechBtn.classList.add('recording');
            speechBtn.innerHTML = '<i class="fas fa-stop"></i>';
            speechBtn.title = 'Click to stop recording';
            
        } catch (error) {
            console.error('Error accessing microphone:', error);
            alert('Could not access microphone. Please check permissions.');
        }
    } else {
        // Stop recording
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
        }
        isRecording = false;
        speechBtn.classList.remove('recording');
        speechBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        speechBtn.title = 'Click to record your symptoms';
    }
}

async function processSpeechToText(audioBlob) {
    try {
        const languageSelect = document.getElementById('language-select');
        const language = languageSelect.value;
        
        // Show loading
        const speechBtn = document.querySelector('.speech-btn');
        speechBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        speechBtn.disabled = true;
        
        // Create form data
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');
        formData.append('language', language);
        
        // Send to backend
        const response = await fetch(`${API_BASE_URL}/speech-to-text`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success && result.data.text) {
            // Add transcribed text to symptoms input
            const symptomsInput = document.getElementById('symptoms-input');
            const currentText = symptomsInput.value.trim();
            const newText = result.data.text.trim();
            
            if (currentText) {
                symptomsInput.value = currentText + ' ' + newText;
            } else {
                symptomsInput.value = newText;
            }
            
            // Show success message
            showNotification('Speech recognized successfully!', 'success');
        } else {
            throw new Error(result.error || 'Speech recognition failed');
        }
        
    } catch (error) {
        console.error('Speech recognition error:', error);
        showNotification('Speech recognition failed. Please try again.', 'error');
    } finally {
        // Reset button
        const speechBtn = document.querySelector('.speech-btn');
        speechBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        speechBtn.disabled = false;
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add CSS for notifications
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 100px;
                right: 20px;
                padding: 1rem 1.5rem;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                z-index: 1000;
                animation: slideInRight 0.3s ease-out;
            }
            .notification-success {
                background: var(--primary-green);
            }
            .notification-error {
                background: var(--danger);
            }
            .notification-info {
                background: var(--primary-blue);
            }
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function toggleNavbar() {
    navMenu.classList.toggle('active');
    navToggle.classList.toggle('active');
}

function handleNavbarScroll() {
    if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
}

function setupSmoothScrolling() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                // Close mobile menu if open
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
    });
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

function initializeScrollReveal() {
    // Scroll reveal animation
    const revealElements = document.querySelectorAll('.health-tile, .language-card, .contact-item, .about-text, .about-image');
    
    function revealOnScroll() {
        const windowHeight = window.innerHeight;
        const elementVisible = 150;
        
        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            
            if (elementTop < windowHeight - elementVisible) {
                element.classList.add('reveal', 'active');
            }
        });
    }
    
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Check on load
}

async function handleSymptomsSubmit(e) {
    e.preventDefault();
    
    const symptomsInput = document.getElementById('symptoms-input');
    const languageSelect = document.getElementById('language-select');
    
    const symptoms = symptomsInput.value.trim();
    const language = languageSelect.value;
    
    if (!symptoms) {
        alert('Please describe your symptoms');
        return;
    }
    
    // Show loading
    loadingElement.classList.remove('hidden');
    resultElement.classList.add('hidden');
    
    try {
        // Call backend API
        const response = await fetch(`${API_BASE_URL}/analyze-symptoms`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                symptoms: symptoms,
                language: language,
                user_id: generateUserId()
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Add to history
            addToHistory(symptoms, language, result.data);
            
            // Show result
            displayResult(result.data);
        } else {
            throw new Error(result.error || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Error processing symptoms:', error);
        alert('Sorry, there was an error processing your request. Please try again.');
    } finally {
        loadingElement.classList.add('hidden');
    }
}

function generateUserId() {
    // Generate a simple user ID for session tracking
    let userId = localStorage.getItem('nirogai_user_id');
    if (!userId) {
        userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('nirogai_user_id', userId);
    }
    return userId;
}

function displayResult(data) {
    const resultContent = document.getElementById('result-content');

    // Get the main analysis text from the AI response
    const analysisText = data.analysis;

    // Convert the AI's formatting (newlines, bolding) into real HTML
    // This turns newlines into line breaks
    let formattedHtml = analysisText.replace(/\n/g, '<br>');
    // This turns **text** into bold text
    formattedHtml = formattedHtml.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Create the final HTML to display on the page
    // This uses the new formatted text
    resultContent.innerHTML = `
        <div class="result-summary">
            <h4>AI Analysis Result</h4>
            <div class="analysis-content">
                ${formattedHtml}
            </div>
        </div>
    `;
    
    // Show the result section
    resultElement.classList.remove('hidden');
    
    // Scroll to the result
    resultElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function addToHistory(symptoms, language, analysisData) {
    const historyItem = {
        id: Date.now(),
        symptoms: symptoms,
        language: language,
        analysis: analysisData,
        timestamp: new Date().toLocaleString()
    };
    
    searchHistory.unshift(historyItem);
    
    // Keep only last 5 searches
    if (searchHistory.length > 5) {
        searchHistory = searchHistory.slice(0, 5);
    }
    
    // Save to localStorage
    localStorage.setItem('nirogai_history', JSON.stringify(searchHistory));
    
    // Update display
    displaySearchHistory();
}

function displaySearchHistory() {
    if (searchHistory.length === 0) {
        historyList.innerHTML = '<p class="no-history">No recent searches</p>';
        return;
    }
    
    historyList.innerHTML = searchHistory.map(item => `
        <div class="history-item" onclick="loadHistoryItem(${item.id})">
            <div class="history-symptoms">${item.symptoms.substring(0, 50)}${item.symptoms.length > 50 ? '...' : ''}</div>
            <div class="history-meta">
                <span class="history-language">${item.language}</span>
                <span class="history-time">${item.timestamp}</span>
            </div>
        </div>
    `).join('');
}

function loadHistoryItem(id) {
    const item = searchHistory.find(h => h.id === id);
    if (item) {
        document.getElementById('symptoms-input').value = item.symptoms;
        document.getElementById('language-select').value = item.language;
        
        // Show previous result
        displayResult(item.analysis);
        
        // Scroll to form
        document.getElementById('symptoms').scrollIntoView({ behavior: 'smooth' });
    }
}

function handleContactSubmit(e) {
    e.preventDefault();
    
    // Simulate form submission
    const submitBtn = e.target.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        alert('Thank you for your message! We will get back to you soon.');
        e.target.reset();
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }, 2000);
}

function changeLanguage(lang) {
    currentLanguage = lang;
    updateLanguage(lang);
    
    // Update active language card
    document.querySelectorAll('.language-card').forEach(card => {
        card.classList.remove('active');
    });
    event.target.closest('.language-card').classList.add('active');
    
    // Save preference
    localStorage.setItem('nirogai_language', lang);
}

function updateLanguage(lang) {
    const elements = document.querySelectorAll('[data-translate]');
    const placeholderElements = document.querySelectorAll('[data-translate-placeholder]');
    
    elements.forEach(element => {
        const key = element.getAttribute('data-translate');
        const translation = getTranslation(key, lang);
        if (translation) {
            element.textContent = translation;
        }
    });
    
    placeholderElements.forEach(element => {
        const key = element.getAttribute('data-translate-placeholder');
        const translation = getTranslation(key, lang);
        if (translation) {
            element.placeholder = translation;
        }
    });
}

function getTranslation(key, lang) {
    const keys = key.split('.');
    let translation = translations[lang];
    
    for (const k of keys) {
        if (translation && translation[k]) {
            translation = translation[k];
        } else {
            // Fallback to English
            translation = translations.en;
            for (const k of keys) {
                if (translation && translation[k]) {
                    translation = translation[k];
                } else {
                    return null;
                }
            }
            break;
        }
    }
    
    return translation;
}

async function openHealthModal(topic) {
    const modalBody = document.getElementById('modal-body');
    
    try {
        // Show loading
        modalBody.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading health information...</p></div>';
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        
        // Get health information from backend
        const response = await fetch(`${API_BASE_URL}/health-info/${topic}?lang=${currentLanguage}`);
        const result = await response.json();
        
        if (result.success) {
            modalBody.innerHTML = `
                <h2>${result.data.title}</h2>
                <div class="health-content">${result.data.content.replace(/\n/g, '<br>')}</div>
            `;
        } else {
            throw new Error(result.error || 'Failed to load health information');
        }
        
    } catch (error) {
        console.error('Error loading health info:', error);
        modalBody.innerHTML = `
            <h2>Error</h2>
            <p>Sorry, we couldn't load the health information at this time. Please try again later.</p>
        `;
    }
}

function closeHealthModal() {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function handleKeyboardNavigation(e) {
    // ESC key to close modal
    if (e.key === 'Escape' && modal.style.display === 'block') {
        closeHealthModal();
    }
}

// Load saved language preference
document.addEventListener('DOMContentLoaded', function() {
    const savedLanguage = localStorage.getItem('nirogai_language');
    if (savedLanguage && translations[savedLanguage]) {
        currentLanguage = savedLanguage;
        updateLanguage(currentLanguage);
        
        // Update active language card
        const languageCards = document.querySelectorAll('.language-card');
        languageCards.forEach(card => {
            if (card.onclick.toString().includes(savedLanguage)) {
                card.classList.add('active');
            }
        });
    }
});

// Add some utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimize scroll performance
window.addEventListener('scroll', debounce(function() {
    handleNavbarScroll();
}, 10));

// Add loading states for better UX
function addLoadingState(element, originalText) {
    element.disabled = true;
    element.textContent = 'Loading...';
    
    return function removeLoadingState() {
        element.disabled = false;
        element.textContent = originalText;
    };
}

// Add error handling for network requests
function handleNetworkError(error) {
    console.error('Network error:', error);
    alert('Network error. Please check your connection and try again.');
}

// Add analytics tracking (placeholder)
function trackEvent(eventName, eventData) {
    console.log('Analytics event:', eventName, eventData);
    // This would be replaced with actual analytics implementation
}

// Performance monitoring
function measurePerformance(name, fn) {
    const start = performance.now();
    const result = fn();
    const end = performance.now();
    console.log(`${name} took ${end - start} milliseconds`);
    return result;
}

console.log('NirogAI application initialized successfully with backend integration');

