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
MODEL_NAME = "microsoft/DialoGPT-medium"  # Better conversational model
tokenizer = None
model = None

# Conversation memory
conversation_history = []
MAX_HISTORY = 10  # Keep last 10 exchanges

def load_model():
    global tokenizer, model
    if tokenizer is None or model is None:
        print("Loading conversational AI model...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        # Add padding token if it doesn't exist
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        # Use CPU for now to avoid accelerate issues
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, 
            torch_dtype=torch.float32,  # Use float32 for CPU
            low_cpu_mem_usage=True
        )
        print("Conversational AI model loaded successfully!")

def add_to_history(user_input, assistant_response):
    """Add conversation to history and maintain max length"""
    global conversation_history
    conversation_history.append({"user": user_input, "assistant": assistant_response})
    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)

def build_conversation_context():
    """Build conversation context from history"""
    if not conversation_history:
        return ""
    
    context = ""
    for exchange in conversation_history[-5:]:  # Use last 5 exchanges for context
        context += f"Human: {exchange['user']}\nAssistant: {exchange['assistant']}\n"
    return context

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
        "stackoverflow", "calculator", "notepad", "file_explorer", "date",
        "compose_email", "send_email"
    ]
    
    if intent in action_intents:
        try:
            action_response = handle_intent(intent, user_input)
            return Response(f"data: {action_response}\n\n", mimetype='text/event-stream')
        except Exception as e:
            return Response(f"data: Error performing action: {str(e)}\n\n", mimetype='text/event-stream')
    
    # Simple responses for common intents
    elif intent == "greeting":
        greeting_response = "Hello! I'm your AI assistant. I can help you with various tasks like opening apps, answering questions, or just having a conversation. How can I assist you today?"
        add_to_history(user_input, greeting_response)
        return Response(f"data: {greeting_response}\n\n", mimetype='text/event-stream')
    elif intent == "conversation":
        # Route conversation intents to AI model
        pass  # Will fall through to AI model
    elif intent == "help":
        help_text = """I can help you with many things! Here are some commands you can try:

🌐 **Web Apps:** YouTube, WhatsApp, Gmail, Google, Facebook, Instagram, Twitter, Netflix, Spotify, GitHub, Stack Overflow

🖥️ **System Apps:** Calculator, Notepad, File Explorer

📧 **Email:** Compose email, Send email, Write email

📅 **Information:** Weather, Time, Date

💬 **General:** Just ask me anything!

Try saying: "open youtube", "compose email to john@example.com", "what's the weather", etc."""
        return Response(f"data: {help_text}\n\n", mimetype='text/event-stream')
    
    # For general conversation, use the AI model
    try:
        load_model()
        
        # Build conversation context
        context = build_conversation_context()
        
        # Create a more natural conversation prompt
        if context:
            prompt = f"{context}Human: {user_input}\nAssistant:"
        else:
            prompt = f"Human: {user_input}\nAssistant:"
        
        # Tokenize the prompt
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        
        # Create streamer for token-by-token output
        streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
        
        # Generate response with better parameters
        generation_kwargs = {
            **inputs,
            "streamer": streamer,
            "max_new_tokens": 150,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.9,
            "repetition_penalty": 1.1,
            "pad_token_id": tokenizer.eos_token_id
        }
        
        # Generate asynchronously
        thread = Thread(target=model.generate, kwargs=generation_kwargs)
        thread.start()

        def generate_stream():
            full_response = ""
            for chunk in streamer:
                if chunk.strip():  # Only yield non-empty chunks
                    full_response += chunk
                    yield f"data: {chunk}\n\n"
            
            # Add to conversation history
            add_to_history(user_input, full_response.strip())
            yield "data: [END]\n\n"

        return Response(generate_stream(), mimetype='text/event-stream')
    
    except Exception as e:
        # Enhanced fallback response with better conversation
        print(f"AI Model Error: {e}")
        
        # Try to provide a helpful response based on the input
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['ai', 'artificial intelligence', 'machine learning']):
            fallback_response = "Artificial Intelligence (AI) is a branch of computer science that focuses on creating systems that can perform tasks that typically require human intelligence. This includes learning, reasoning, problem-solving, perception, and language understanding. AI has applications in many fields like healthcare, finance, transportation, and entertainment. Would you like me to explain any specific aspect of AI?"
        
        elif any(word in user_lower for word in ['how are you', 'how do you do']):
            fallback_response = "I'm doing well, thank you for asking! I'm here to help you with various tasks like opening applications, answering questions, composing emails, and having conversations. How can I assist you today?"
        
        elif any(word in user_lower for word in ['explain', 'what is', 'tell me about']):
            fallback_response = f"I'd be happy to explain that topic! However, my AI model is currently loading. In the meantime, I can help you with specific commands like 'open youtube', 'compose email', 'what's the weather', or 'help' for more options. What would you like to know about?"
        
        else:
            fallback_response = f"I understand you're asking about '{user_input}'. My AI model is currently loading, but I can still help you with specific commands like 'open youtube', 'compose email', 'what's the weather', or 'help' for more options!"
        
        add_to_history(user_input, fallback_response)
        return Response(f"data: {fallback_response}\n\n", mimetype='text/event-stream')

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

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return {"status": "success", "message": "Conversation history cleared"}

# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    # Make sure to run from project root
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
