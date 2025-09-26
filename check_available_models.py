import google.generativeai as genai
from config import get_gemini_api_key

# Configure the API
api_key = get_gemini_api_key()
if not api_key:
    print("No API key found")
    exit(1)

print(f"Using API key: {api_key[:10]}...")

try:
    genai.configure(api_key=api_key)
    
    # List available models
    print("Available models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
            
except Exception as e:
    print(f"Error: {e}")