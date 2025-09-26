import google.generativeai as genai
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the config module
from config import get_gemini_api_key

def list_models_with_key():
    # Get the API key
    api_key = get_gemini_api_key()
    print(f"API Key (first 15 chars): {api_key[:15] if api_key else 'None'}")

    if not api_key:
        print("No API key found!")
        return

    try:
        genai.configure(api_key=api_key)
        print("API configured successfully")
        
        # Try to list available models
        print("\nTrying to list available models...")
        try:
            models_found = []
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    print(f"Available model: {model.name}")
                    models_found.append(model.name)
            return models_found
        except Exception as e:
            print(f"Could not list models: {e}")
            return []
            
    except Exception as e:
        print(f"Configuration error: {e}")
        return []

if __name__ == "__main__":
    list_models_with_key()