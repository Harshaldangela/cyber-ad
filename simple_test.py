import google.generativeai as genai
from config import get_gemini_api_key

# Get the API key
api_key = get_gemini_api_key()
print(f"API Key (first 10 chars): {api_key[:10] if api_key else 'None'}")

if not api_key:
    print("No API key found!")
    exit(1)

try:
    genai.configure(api_key=api_key)
    print("API configured successfully")
    
    # Try to list available models
    print("Trying to list models...")
    models = genai.list_models()
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"Available model: {model.name}")
            
except Exception as e:
    print(f"Error: {e}")
    if "429" in str(e):
        print("This indicates a quota exceeded error - you've used up your API quota")