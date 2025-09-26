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

app = FastAPI(title="Improved Cyber Awareness Ad API")

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

def get_model():
    api_key = get_gemini_api_key()
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    genai.configure(api_key=api_key)
    for name in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]:
        try:
            model = genai.GenerativeModel(name)
            model.generate_content("Hello")
            return model
        except Exception:
            continue
    raise HTTPException(status_code=500, detail="No compatible Gemini model found")

# Load improved classifier and vectorizer
try:
    _tfidf = pickle.load(open('improved_vectorizer.pkl', 'rb'))
    _clf = pickle.load(open('improved_model.pkl', 'rb'))
    print("Improved model loaded successfully!")
except Exception as e:
    print(f"Error loading improved model: {e}")
    # Fallback to original model
    try:
        _tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
        _clf = pickle.load(open('model.pkl', 'rb'))
        print("Fallback to original model")
    except Exception as e2:
        print(f"Error loading original model: {e2}")
        _tfidf = None
        _clf = None

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
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
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

class AnalyzeRequest(BaseModel):
    text: str
    languages: list[str] | None = None

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    if _tfidf is None or _clf is None:
        raise HTTPException(status_code=500, detail="Classifier not available on server")
    try:
        # Preprocess the text
        transformed = advanced_text_preprocessing(req.text)
        
        # Transform and predict
        vec = _tfidf.transform([transformed])
        pred = _clf.predict(vec)[0]
        prob = _clf.predict_proba(vec)[0]
        
        # Get confidence score
        confidence = max(prob)
        
        label = 'spam' if int(pred) == 1 else 'not_spam'

        result: dict = {
            "classification": label,
            "confidence": float(confidence)
        }
        
        if label == 'spam':
            model = get_model()
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
        "model_loaded": _tfidf is not None and _clf is not None
    }

# Run with: uvicorn improved_api:app --reload --port 8000