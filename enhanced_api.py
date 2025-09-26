from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from config import get_gemini_api_key
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

app = FastAPI(title="Enhanced Cyber Awareness Ad API")

# Ensure UTF-8 encoding
import sys
import os
if sys.getdefaultencoding() != 'utf-8':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# CORS - adjust origins as needed (e.g., your extension's origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    text: str

class TranslateRequest(BaseModel):
    ad_text: str
    languages: list[str]

class AnalyzeRequest(BaseModel):
    text: str
    languages: list[str] | None = None

def get_model():
    api_key = get_gemini_api_key()
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    genai.configure(api_key=api_key)
    
    # Try different model names, prioritizing the one that works
    # Based on our testing, models/gemini-2.0-flash is working
    for name in [
        "models/gemini-2.0-flash",  # This one works based on our testing
        "models/gemini-2.0-flash-001",
        "models/gemini-1.5-flash-latest",
        "models/gemini-1.5-flash-002", 
        "models/gemini-1.5-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro"
    ]:
        try:
            model = genai.GenerativeModel(name)
            # Test the model with a simple prompt
            model.generate_content("Hello", request_options={"timeout": 10})
            print(f"Successfully loaded model: {name}")
            return model
        except Exception as e:
            print(f"Failed to load model {name}: {e}")
            # If we get a quota error, don't try other models
            if "429" in str(e):
                raise HTTPException(status_code=429, detail="API quota exceeded. Please try again later or configure your own API key with higher quotas.")
            continue
    # If all models fail, return None to indicate no model is available
    print("All models failed to load, returning None")
    return None

# Load improved classifier and vectorizer
try:
    _tfidf = pickle.load(open('robust_vectorizer.pkl', 'rb'))
    _clf = pickle.load(open('robust_model.pkl', 'rb'))
    print("Robust model loaded successfully!")
except Exception as e:
    print(f"Error loading robust model: {e}")
    # Fallback to original model
    try:
        _tfidf = pickle.load(open('improved_vectorizer.pkl', 'rb'))
        _clf = pickle.load(open('improved_model.pkl', 'rb'))
        print("Fallback to improved model")
    except Exception as e2:
        print(f"Error loading improved model: {e2}")
        # Final fallback to original model
        try:
            _tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
            _clf = pickle.load(open('model.pkl', 'rb'))
            print("Fallback to original model")
        except Exception as e3:
            print(f"Error loading original model: {e3}")
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

def _generate_ad(model, text: str) -> str:
    prompt = f"""
    Create a highly creative, engaging, and visually appealing cyber awareness advertisement derived from this spam message: "{text}".
    
    Make it fun, memorable, and shareable on social media. Use modern marketing language and creative storytelling.
    
    Output PLAIN TEXT only (no markdown symbols, no **, no #). Use this exact structure and labels:
    Headline: <6-10 word catchy headline with emojis>
    Ad Content:
    - <short engaging point 1 with emoji>
    - <short engaging point 2 with emoji>
    - <short engaging point 3 with emoji>
    Key Takeaway: <one-sentence main rule with emoji>
    Call to Action: <one short instruction with emoji>
    """
    resp = model.generate_content(prompt)
    return resp.text

def hybrid_spam_detection(text: str) -> Tuple[int, float]:
    """
    Improved hybrid spam detection combining ML model and rule-based approach
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
    
    # Improved combination logic
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

@app.post("/generate-ad")
async def generate_ad(req: GenerateRequest):
    try:
        model = get_model()
        ad = _generate_ad(model, req.text)
        return {"ad": ad}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate")
async def translate(req: TranslateRequest):
    try:
        model = get_model()
        translations = {}
        for lang in req.languages:
            prompt = f"""
            Translate the following content into {lang}. Preserve Markdown structure and headings:
            **Headline:**
            **Ad Content:**
            **Key Takeaway:**
            **Call to Action:**
            ---
            {req.ad_text}
            """
            resp = model.generate_content(prompt)
            translations[lang] = resp.text
        return {"translations": translations}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    try:
        # Log the received text for debugging
        print(f"DEBUG: Received text: '{req.text}'")
        print(f"DEBUG: Text length: {len(req.text)}")
        
        # Use hybrid detection
        pred, confidence = hybrid_spam_detection(req.text)
        label = 'spam' if pred == 1 else 'not_spam'

        result: dict = {
            "classification": label,
            "confidence": float(confidence)
        }
        
        if label == 'spam':
            try:
                model = get_model()
                if model is not None:
                    ad_text = _generate_ad(model, req.text)
                    result["ad"] = ad_text
                    if req.languages:
                        translations = {}
                        for lang in req.languages:
                            tprompt = f"""
                            Translate the following ad into {lang}. Preserve labels and bullets. Output PLAIN TEXT only (no markdown symbols).
                            {ad_text}
                            """
                            tmodel = model
                            tresp = tmodel.generate_content(tprompt)
                            translations[lang] = tresp.text
                        result["translations"] = translations
                else:
                    result["ad_generation_error"] = "Ad generation service is temporarily unavailable. This may be due to API quota limitations or model access issues."
            except HTTPException as he:
                # Re-raise HTTP exceptions (like quota errors)
                raise he
            except Exception as e:
                # If ad generation fails, continue without it but provide a clear message
                print(f"Ad generation failed: {e}")
                result["ad_generation_error"] = "Unable to generate cyber awareness ad at this time. This may be due to API quota limitations or model access issues."
                pass
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
        "rule_detector_loaded": True,
        "improved_rule_detector": True
    }

# Test endpoint
@app.post("/test-detection")
async def test_detection(req: GenerateRequest):
    """Test endpoint to see individual model predictions"""
    try:
        # Get ML model prediction if available
        ml_prediction = None
        ml_confidence = 0.0
        
        if _tfidf is not None and _clf is not None:
            try:
                # Preprocess the text
                transformed = advanced_text_preprocessing(req.text)
                
                # Transform and predict
                vec = _tfidf.transform([transformed])
                ml_prediction = _clf.predict(vec)[0]
                prob = _clf.predict_proba(vec)[0]
                ml_confidence = max(prob)
            except Exception as e:
                print(f"ML model prediction error: {e}")
        
        # Get rule-based prediction
        rule_prediction, rule_confidence = _rule_detector.predict(req.text)
        
        # Get hybrid prediction
        hybrid_prediction, hybrid_confidence = hybrid_spam_detection(req.text)
        
        return {
            "text": req.text,
            "ml_model": {
                "prediction": int(ml_prediction) if ml_prediction is not None else None,
                "confidence": float(ml_confidence) if ml_prediction is not None else 0.0
            },
            "rule_based": {
                "prediction": int(rule_prediction),
                "confidence": float(rule_confidence)
            },
            "hybrid": {
                "prediction": int(hybrid_prediction),
                "confidence": float(hybrid_confidence)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn enhanced_api:app --reload --port 8000