import sys, os
from flask import Flask, request, Response, send_from_directory
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
import torch
from threading import Thread

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models.intent_model import IntentPredictor
from preprocessing.text_utils import clean_text
from actions.action_router import handle_intent

# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__, static_folder='../frontend')
CORS(app)  # Enable CORS for all routes

# -----------------------------
# Load models
# -----------------------------
MODEL_NAME = "microsoft/DialoGPT-small"  # Much smaller and faster model
tokenizer = None
model = None

def load_model():
    global tokenizer, model
    if tokenizer is None or model is None:
        print("Loading Mistral model...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        # Use CPU for now to avoid accelerate issues
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, 
            torch_dtype=torch.float32,  # Use float32 for CPU
            low_cpu_mem_usage=True
        )
        print("Model loaded successfully!")

# Intent Predictor (replace paths with your trained files)
intent_predictor = IntentPredictor(
    os.path.join(PROJECT_ROOT, "models", "intent_model.pkl"),
    os.path.join(PROJECT_ROOT, "models", "tfidf.pkl"),
    os.path.join(PROJECT_ROOT, "models", "labels.pkl")
)

# -----------------------------
# Streaming route
# -----------------------------
@app.route('/stream', methods=['GET'])
def stream_chat():
    user_input = request.args.get("text", "")
    if not user_input:
        return "No text provided", 400

    cleaned = clean_text(user_input)
    intent = intent_predictor.predict_intent(cleaned)
    
    # Handle specific actions first
    action_intents = [
        "weather", "music", "youtube", "time", "whatsapp", "gmail", "google", 
        "facebook", "instagram", "twitter", "netflix", "spotify", "github", 
        "stackoverflow", "calculator", "notepad", "file_explorer", "date"
    ]
    
    if intent in action_intents:
        try:
            action_response = handle_intent(intent, user_input)
            return Response(f"data: {action_response}\n\n", mimetype='text/event-stream')
        except Exception as e:
            return Response(f"data: Error performing action: {str(e)}\n\n", mimetype='text/event-stream')
    
    # Simple responses for common intents
    elif intent == "greeting":
        return Response(f"data: Hello! How can I help you today?\n\n", mimetype='text/event-stream')
    elif intent == "help":
        help_text = """I can help you with many things! Here are some commands you can try:

🌐 **Web Apps:** YouTube, WhatsApp, Gmail, Google, Facebook, Instagram, Twitter, Netflix, Spotify, GitHub, Stack Overflow

🖥️ **System Apps:** Calculator, Notepad, File Explorer

📅 **Information:** Weather, Time, Date

💬 **General:** Just ask me anything!

Try saying: "open youtube", "what's the weather", "open calculator", etc."""
        return Response(f"data: {help_text}\n\n", mimetype='text/event-stream')
    
    # For other intents, try to load the model
    try:
        load_model()
        
        # Create streamer for token-by-token output
        streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
        inputs = tokenizer(f"User: {user_input}\nAssistant:", return_tensors="pt")

        # Generate asynchronously
        thread = Thread(target=model.generate, kwargs=dict(
            **inputs, streamer=streamer, max_new_tokens=100
        ))
        thread.start()

        def generate_stream():
            for chunk in streamer:
                yield f"data: {chunk}\n\n"
            yield "data: [END]\n\n"

        return Response(generate_stream(), mimetype='text/event-stream')
    
    except Exception as e:
        # Fallback response if model fails
        return Response(f"data: I'm still loading my AI model. For now, I can tell you that you asked: '{user_input}'. Please wait a moment and try again!\n\n", mimetype='text/event-stream')

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
    return {"status": "running", "message": "Mistral Streaming API is running..."}

# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    # Make sure to run from project root
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
