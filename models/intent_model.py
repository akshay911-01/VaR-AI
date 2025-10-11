# models/intent_model.py
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import numpy as np

class IntentPredictor:
    def __init__(self, model_path=None, vectorizer_path=None, labels_path=None):
        """
        Initialize the IntentPredictor with optional model files.
        If files don't exist, creates a simple fallback predictor.
        """
        self.model = None
        self.vectorizer = None
        self.labels = None
        
        # Try to load existing models
        if model_path and os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"Loaded intent model from {model_path}")
            except Exception as e:
                print(f"Failed to load model from {model_path}: {e}")
        
        if vectorizer_path and os.path.exists(vectorizer_path):
            try:
                with open(vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                print(f"Loaded vectorizer from {vectorizer_path}")
            except Exception as e:
                print(f"Failed to load vectorizer from {vectorizer_path}: {e}")
        
        if labels_path and os.path.exists(labels_path):
            try:
                with open(labels_path, 'rb') as f:
                    self.labels = pickle.load(f)
                print(f"Loaded labels from {labels_path}")
            except Exception as e:
                print(f"Failed to load labels from {labels_path}: {e}")
        
        # If any component is missing, create a simple fallback
        if not all([self.model, self.vectorizer, self.labels]):
            self._create_fallback_predictor()
    
    def _create_fallback_predictor(self):
        """Create a simple rule-based intent predictor as fallback"""
        print("Creating fallback intent predictor...")
        
        # Simple keyword-based intent detection
        self.intent_keywords = {
            'weather': ['weather', 'temperature', 'rain', 'sunny', 'cloudy', 'forecast', 'climate'],
            'music': ['play music', 'play song', 'play artist', 'play album'],
            'youtube': ['youtube', 'open youtube', 'watch video', 'video', 'youtube.com'],
            'whatsapp': ['whatsapp', 'open whatsapp', 'message', 'chat', 'whatsapp web'],
            'gmail': ['gmail', 'open gmail', 'google mail'],
            'compose_email': ['compose email', 'write email', 'draft email', 'create email', 'type email', 'email to', 'send email to', 'compose a mail', 'write a mail', 'compose mail', 'write mail'],
            'send_email': ['send email', 'email send', 'mail send'],
            'google': ['google', 'open google', 'search', 'google.com'],
            'facebook': ['facebook', 'open facebook', 'fb', 'facebook.com'],
            'instagram': ['instagram', 'open instagram', 'insta', 'instagram.com'],
            'twitter': ['twitter', 'open twitter', 'tweet', 'twitter.com', 'x.com'],
            'netflix': ['netflix', 'open netflix', 'watch movie', 'stream', 'netflix.com'],
            'spotify': ['spotify', 'open spotify', 'spotify.com'],
            'github': ['github', 'open github', 'git', 'github.com'],
            'stackoverflow': ['stackoverflow', 'open stackoverflow', 'stack overflow', 'stackoverflow.com'],
            'calculator': ['calculator', 'open calculator', 'calc', 'calculate'],
            'notepad': ['notepad', 'open notepad', 'text editor', 'write', 'note'],
            'file_explorer': ['file explorer', 'open file explorer', 'files', 'folder', 'explorer'],
            'time': ['time', 'clock', 'what time', 'current time'],
            'date': ['date', 'what date', 'today', 'current date'],
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'how are you', 'how do you do'],
            'help': ['help', 'assist', 'support', 'what can you do', 'commands', 'what are your capabilities'],
            'conversation': ['tell me', 'explain', 'what is', 'how does', 'why', 'can you', 'do you know', 'i want to know', 'i need help with']
        }
        
        self.default_intent = 'general'
    
    def predict_intent(self, text):
        """
        Predict intent for the given text.
        Returns the predicted intent label.
        """
        if self.model and self.vectorizer and self.labels:
            # Use trained model
            try:
                text_vectorized = self.vectorizer.transform([text])
                prediction = self.model.predict(text_vectorized)[0]
                confidence = self.model.predict_proba(text_vectorized).max()
                
                if confidence > 0.5:  # Only return prediction if confident
                    return self.labels[prediction]
            except Exception as e:
                print(f"Error in model prediction: {e}")
        
        # Fallback to keyword-based detection with priority for longer matches
        text_lower = text.lower()
        
        # Sort keywords by length (longest first) to prioritize specific matches
        intent_matches = []
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    intent_matches.append((intent, len(keyword)))
        
        # Return the intent with the longest matching keyword
        if intent_matches:
            intent_matches.sort(key=lambda x: x[1], reverse=True)
            return intent_matches[0][0]
        
        return self.default_intent
    
    def get_confidence(self, text):
        """Get confidence score for intent prediction"""
        if self.model and self.vectorizer:
            try:
                text_vectorized = self.vectorizer.transform([text])
                confidence = self.model.predict_proba(text_vectorized).max()
                return confidence
            except:
                pass
        
        # For fallback, return 1.0 if keyword match found, 0.5 otherwise
        text_lower = text.lower()
        for keywords in self.intent_keywords.values():
            if any(keyword in text_lower for keyword in keywords):
                return 1.0
        return 0.5
