import google.generativeai as genai
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the config module
from config import get_gemini_api_key

def list_available_models():
    # Get the API key
    api_key = get_gemini_api_key()
    print(f"API Key (first 10 chars): {api_key[:10] if api_key else 'None'}")

    if not api_key:
        print("No API key found!")
        return

    try:
        genai.configure(api_key=api_key)
        print("API configured successfully")
        
        # Try to list available models
        print("\nTrying to list available models...")
        try:
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    print(f"Available model: {model.name}")
        except Exception as e:
            print(f"Could not list models: {e}")
            
        # Test specific working model names based on current documentation
        print("\nTesting known working model names:")
        working_models = []
        test_models = [
            "gemini-1.5-flash-001",
            "gemini-1.5-flash-002",
            "gemini-1.5-pro-001",
            "gemini-1.5-pro-002",
            "gemini-pro",
            "gemini-1.0-pro-001",
            "gemini-1.0-pro-002"
        ]
        
        for model_name in test_models:
            try:
                print(f"Testing: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Hi", request_options={"timeout": 10})
                print(f"  SUCCESS: {model_name}")
                working_models.append(model_name)
                # Break after first success since we know quota is an issue
                break
            except Exception as e:
                print(f"  FAILED: {model_name} - {str(e)[:100]}")
        
        print(f"\nFirst working model found: {working_models[0] if working_models else 'None'}")
        
    except Exception as e:
        print(f"Configuration error: {e}")

if __name__ == "__main__":
    list_available_models()