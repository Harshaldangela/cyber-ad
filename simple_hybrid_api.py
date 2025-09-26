from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import re
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
from typing import Tuple
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the improved rule-based detector
from improved_rule_based_detector import ImprovedRuleBasedSpamDetector

app = FastAPI(title="Simple Hybrid Spam Detection API")

# CORS - adjust origins as needed (e.g., your extension's origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str

# Load improved classifier and vectorizer
try:
    _tfidf = pickle.load(open('robust_vectorizer.pkl', 'rb'))
    _clf = pickle.load(open('robust_model.pkl', 'rb'))
    print("Robust model loaded successfully!")
except Exception as e:
    print(f"Error loading robust model: {e}")
    _tfidf = None
    _clf = None

# Initialize improved rule-based detector
_rule_detector = ImprovedRuleBasedSpamDetector()
_ps = PorterStemmer()

def advanced_text_preprocessing(text: str) -> str:
    """Advanced text preprocessing for better feature extraction"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove phone numbers
    text = re.sub(r'\d{3,}', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize
    tokens = nltk.word_tokenize(text)
    
    # Remove punctuation and non-alphabetic tokens
    tokens = [token for token in tokens if token.isalpha() and len(token) > 1]
    
    # Remove stopwords
    try:
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
    except:
        # Fallback if stopwords not available
        pass
    
    # Stemming
    tokens = [_ps.stem(token) for token in tokens]
    
    return " ".join(tokens)

def final_improved_hybrid_spam_detection(text: str) -> Tuple[int, float]:
    """
    Final improved hybrid spam detection combining ML model and rule-based approach
    Returns: (prediction, confidence) where prediction is 1 for spam, 0 for ham
    """
    # Get ML model prediction if available
    ml_prediction = None
    ml_confidence = 0.0
    
    if _tfidf is not None and _clf is not None:
        try:
            # Preprocess the text
            transformed = advanced_text_preprocessing(text)
            
            # Transform and predict
            vec = _tfidf.transform([transformed])
            ml_prediction = _clf.predict(vec)[0]
            prob = _clf.predict_proba(vec)[0]
            ml_confidence = max(prob)
        except Exception as e:
            print(f"ML model prediction error: {e}")
    
    # Get improved rule-based prediction
    rule_prediction, rule_confidence = _rule_detector.predict(text)
    
    # Final improved combination logic
    if ml_prediction is not None:
        # If both models agree, use higher confidence
        if ml_prediction == rule_prediction:
            combined_confidence = max(ml_confidence, rule_confidence)
            final_prediction = ml_prediction
        else:
            # If they disagree, be more aggressive in trusting the improved rule-based detector
            # The improved rule-based detector is more reliable for known spam patterns
            
            # Check if this is a known spam pattern that the rule detector recognizes with confidence
            if rule_confidence > 0.4:  # Moderate confidence from improved rules
                # If rule-based has moderate to high confidence, trust it more
                final_prediction = rule_prediction
                # Boost confidence since we trust the improved rules
                combined_confidence = min(1.0, rule_confidence + 0.15)
            elif ml_confidence > 0.95:  # Very high confidence from ML (only trust if extremely sure)
                # If ML is very confident, trust it
                final_prediction = ml_prediction
                combined_confidence = ml_confidence
            else:
                # Default to rule-based when in doubt, as it's more reliable for spam detection
                final_prediction = rule_prediction
                combined_confidence = rule_confidence
    else:
        # Fallback to rule-based only
        final_prediction = rule_prediction
        combined_confidence = rule_confidence
    
    return int(final_prediction), float(combined_confidence)

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    try:
        # Use final improved hybrid detection
        pred, confidence = final_improved_hybrid_spam_detection(req.text)
        label = 'spam' if pred == 1 else 'not_spam'

        result: dict = {
            "classification": label,
            "confidence": float(confidence)
        }
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": _tfidf is not None and _clf is not None,
        "rule_detector_loaded": True
    }

# Run with: uvicorn simple_hybrid_api:app --reload --port 8003