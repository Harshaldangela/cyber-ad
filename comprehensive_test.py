import pickle
import google.generativeai as genai
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now import the config module
from config import get_gemini_api_key

def test_api_key_and_models():
    # Get the API key
    api_key = get_gemini_api_key()
    print(f"API Key (first 10 chars): {api_key[:10] if api_key else 'None'}")

    if not api_key:
        print("No API key found!")
        return

    try:
        genai.configure(api_key=api_key)
        print("API configured successfully")
        
        # Test current working models
        working_models = []
        test_models = [
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-pro-exp-0827",  # Experimental model
            "models/gemini-1.5-flash",
            "models/gemini-1.5-pro"
        ]
        
        for model_name in test_models:
            try:
                print(f"\nTesting model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say 'Hello' in one word only", request_options={"timeout": 10})
                print(f"  SUCCESS: {response.text.strip()}")
                working_models.append(model_name)
            except Exception as e:
                error_msg = str(e)
                print(f"  FAILED: {error_msg}")
                if "429" in error_msg:
                    print("  *** QUOTA EXCEEDED - This is the main issue ***")
                    break  # No point testing other models if quota is exceeded
        
        print(f"\nWorking models: {working_models}")
        
    except Exception as e:
        print(f"Configuration error: {e}")
        if "429" in str(e):
            print("QUOTA EXCEEDED: You've used up your API quota for this period")

if __name__ == "__main__":
    test_api_key_and_models()
