import sys, os
import subprocess
import webbrowser
from flask import Flask, request, Response, send_from_directory
from flask_cors import CORS

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models.intent_model import IntentPredictor

# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__, static_folder='../frontend')
CORS(app)  # Enable CORS for all routes

# -----------------------------
# Application Opening Functions
# -----------------------------
def open_youtube():
    """Open YouTube in the default browser"""
    try:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube in your browser..."
    except Exception as e:
        return f"Could not open YouTube: {str(e)}"

def open_weather_app():
    """Open weather app or website"""
    try:
        webbrowser.open("https://weather.com")
        return "Opening weather information..."
    except Exception as e:
        return f"Could not open weather app: {str(e)}"

def open_whatsapp():
    """Open WhatsApp Web"""
    try:
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp Web..."
    except Exception as e:
        return f"Could not open WhatsApp: {str(e)}"

def open_calculator():
    """Open Windows Calculator"""
    try:
        subprocess.Popen(["calc.exe"])
        return "Opening Calculator..."
    except Exception as e:
        return f"Could not open Calculator: {str(e)}"

def open_notepad():
    """Open Windows Notepad"""
    try:
        subprocess.Popen(["notepad.exe"])
        return "Opening Notepad..."
    except Exception as e:
        return f"Could not open Notepad: {str(e)}"

def open_file_explorer():
    """Open Windows File Explorer"""
    try:
        subprocess.Popen(["explorer.exe"])
        return "Opening File Explorer..."
    except Exception as e:
        return f"Could not open File Explorer: {str(e)}"

def open_google():
    """Open Google search"""
    try:
        webbrowser.open("https://www.google.com")
        return "Opening Google..."
    except Exception as e:
        return f"Could not open Google: {str(e)}"

def open_gmail():
    """Open Gmail"""
    try:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail..."
    except Exception as e:
        return f"Could not open Gmail: {str(e)}"

def open_spotify():
    """Open Spotify Web Player"""
    try:
        webbrowser.open("https://open.spotify.com")
        return "Opening Spotify..."
    except Exception as e:
        return f"Could not open Spotify: {str(e)}"

def open_netflix():
    """Open Netflix"""
    try:
        webbrowser.open("https://www.netflix.com")
        return "Opening Netflix..."
    except Exception as e:
        return f"Could not open Netflix: {str(e)}"

# Application mapping
APP_FUNCTIONS = {
    'youtube': open_youtube,
    'weather': open_weather_app,
    'whatsapp': open_whatsapp,
    'calculator': open_calculator,
    'notepad': open_notepad,
    'file explorer': open_file_explorer,
    'google': open_google,
    'gmail': open_gmail,
    'spotify': open_spotify,
    'netflix': open_netflix
}

# Intent Predictor (replace paths with your trained files)
intent_predictor = IntentPredictor(
    os.path.join(PROJECT_ROOT, "models", "intent_model.pkl"),
    os.path.join(PROJECT_ROOT, "models", "tfidf.pkl"),
    os.path.join(PROJECT_ROOT, "models", "labels.pkl")
)

# -----------------------------
# Enhanced Intent Recognition
# -----------------------------
def detect_app_to_open(text):
    """Detect which application the user wants to open"""
    text_lower = text.lower()
    
    # Check for specific app names
    for app_name, func in APP_FUNCTIONS.items():
        if app_name in text_lower:
            return app_name, func
    
    # Check for common phrases
    app_phrases = {
        'youtube': ['youtube', 'watch video', 'watch videos'],
        'weather': ['weather', 'weather app', 'weather forecast'],
        'whatsapp': ['whatsapp', 'whats app', 'message'],
        'calculator': ['calculator', 'calc', 'calculate'],
        'notepad': ['notepad', 'text editor', 'write text'],
        'file explorer': ['file explorer', 'files', 'folder', 'open folder'],
        'google': ['google', 'search', 'google search'],
        'gmail': ['gmail', 'email', 'mail'],
        'spotify': ['spotify', 'music', 'play music'],
        'netflix': ['netflix', 'watch movie', 'watch movies']
    }
    
    for app_name, phrases in app_phrases.items():
        if any(phrase in text_lower for phrase in phrases):
            return app_name, APP_FUNCTIONS[app_name]
    
    return None, None

# -----------------------------
# Simple streaming route (no AI model needed)
# -----------------------------
@app.route('/stream', methods=['GET'])
def stream_chat():
    user_input = request.args.get("text", "")
    if not user_input:
        return "No text provided", 400

    cleaned = user_input.lower().strip()  # Simple text cleaning
    
    # First check if user wants to open an app
    app_name, app_func = detect_app_to_open(user_input)
    if app_name and app_func:
        try:
            response_text = app_func()
            # Simulate streaming by sending the response in chunks
            def generate_stream():
                words = response_text.split()
                for i, word in enumerate(words):
                    yield f"data: {word} "
                    if i < len(words) - 1:
                        yield "\n\n"
                yield "data: [END]\n\n"
            return Response(generate_stream(), mimetype='text/event-stream')
        except Exception as e:
            response_text = f"Sorry, I couldn't open {app_name}. Error: {str(e)}"
            def generate_stream():
                words = response_text.split()
                for i, word in enumerate(words):
                    yield f"data: {word} "
                    if i < len(words) - 1:
                        yield "\n\n"
                yield "data: [END]\n\n"
            return Response(generate_stream(), mimetype='text/event-stream')
    
    # If no app detected, use regular intent prediction
    intent = intent_predictor.predict_intent(cleaned)
    
    # Smart responses based on intent
    responses = {
        "weather": "The weather is sunny today! Temperature is around 25°C with light winds.",
        "greeting": "Hello! How can I help you today? I'm your AI assistant!",
        "help": "I can help you open apps like YouTube, WhatsApp, Calculator, Weather, and more! Just ask me to open them.",
        "time": "The current time is " + str(__import__('datetime').datetime.now().strftime("%H:%M:%S")),
        "music": "I'd love to help with music! I can open Spotify for you. Just say 'open spotify' or 'play music'.",
        "general": f"That's an interesting question: '{user_input}'. I can help you open apps like YouTube, WhatsApp, Calculator, Weather, and more!"
    }
    
    response_text = responses.get(intent, responses["general"])
    
    # Simulate streaming by sending the response in chunks
    def generate_stream():
        words = response_text.split()
        for i, word in enumerate(words):
            yield f"data: {word} "
            if i < len(words) - 1:
                yield "\n\n"
        yield "data: [END]\n\n"

    return Response(generate_stream(), mimetype='text/event-stream')

# -----------------------------
# Serve frontend files
# -----------------------------
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# -----------------------------
# API status route
# -----------------------------
@app.route('/api/status')
def api_status():
    return {"status": "running", "message": "Simple AI Assistant is running!"}

# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    print("Starting Simple AI Assistant...")
    print("Frontend available at: http://localhost:5000")
    print("No model loading required - instant responses!")
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
