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
            'weather': ['weather', 'temperature', 'rain', 'sunny', 'cloudy', 'forecast'],
            'music': ['play', 'music', 'song', 'artist', 'album'],
            'time': ['time', 'clock', 'what time', 'current time'],
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
            'help': ['help', 'assist', 'support', 'what can you do']
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
        
        # Fallback to keyword-based detection
        text_lower = text.lower()
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return intent
        
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
