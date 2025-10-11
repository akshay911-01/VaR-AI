# preprocessing/text_utils.py
import re
import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = nltk.word_tokenize(text)
    tokens = [t for t in tokens if t not in STOPWORDS]
    return " ".join(tokens)

def load_intents(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# TF-IDF helper: fit on intents patterns (run when preparing the model)
def build_tfidf_from_intents(intents):
    texts = []
    tags = []
    for intent in intents['intents']:
        for p in intent['patterns']:
            texts.append(clean_text(p))
            tags.append(intent['tag'])
    vec = TfidfVectorizer(max_features=2000)
    X = vec.fit_transform(texts)
    return vec, X, tags
