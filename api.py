from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from config import get_gemini_api_key
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

app = FastAPI(title="Cyber Awareness Ad API")

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


# Load classifier and vectorizer once
try:
    _tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
    _clf = pickle.load(open('model.pkl', 'rb'))
except Exception:
    _tfidf = None
    _clf = None

_ps = PorterStemmer()

def _transform_text(text: str) -> str:
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    alnum = [t for t in tokens if t.isalnum()]
    filtered = [t for t in alnum if t not in stopwords.words('english') and t not in string.punctuation]
    stemmed = [_ps.stem(t) for t in filtered]
    return " ".join(stemmed)


def _generate_ad(model, text: str) -> str:
    prompt = f"""
    Create a concise, audience-friendly cyber awareness advertisement derived from this spam message: "{text}".
    Output PLAIN TEXT only (no markdown symbols, no **, no #). Use this exact structure and labels:
    Headline: <6-10 word catchy headline>
    Ad Content:
    - <short point 1>
    - <short point 2>
    - <short point 3>
    Key Takeaway: <one-sentence main rule>
    Call to Action: <one short instruction>
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
        transformed = _transform_text(req.text)
        vec = _tfidf.transform([transformed])
        pred = _clf.predict(vec)[0]
        label = 'spam' if int(pred) == 1 else 'not_spam'

        result: dict = {"classification": label}
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

# Run with: uvicorn api:app --reload --port 8000
