import google.generativeai as genai
import os
from config import get_gemini_api_key

# Configure the API
api_key = get_gemini_api_key()
if not api_key:
    print("No API key found")
    exit(1)

print(f"Using API key: {api_key[:10]}...")  # Print first 10 chars for verification

genai.configure(api_key=api_key)

# Test different model names
models_to_test = [
    "gemini-2.0-flash",
    "gemini-1.5-flash", 
    "gemini-1.5-pro",
    "gemini-pro",
    "gemini-flash",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro",
    "models/gemini-pro"
]

for model_name in models_to_test:
    try:
        print(f"Testing model: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, world!")
        print(f"  SUCCESS: {model_name}")
        print(f"  Response: {response.text[:50]}...")
        break
    except Exception as e:
        print(f"  FAILED: {model_name} - {str(e)[:100]}")
else:
    print("No compatible models found!")