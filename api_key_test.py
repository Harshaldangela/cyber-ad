import google.generativeai as genai
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the config module
from config import get_gemini_api_key

def test_api_key():
    # Get the API key
    api_key = get_gemini_api_key()
    print(f"API Key (first 15 chars): {api_key[:15] if api_key else 'None'}")

    if not api_key:
        print("No API key found!")
        return

    try:
        genai.configure(api_key=api_key)
        print("API configured successfully")
        
        # Test with the correct model name format
        print("\nTesting with correct model name format:")
        try:
            model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
            response = model.generate_content("Say 'Hello' in one word only", request_options={"timeout": 10})
            print(f"SUCCESS: {response.text.strip()}")
            print("API key is working correctly!")
            return True
        except Exception as e:
            print(f"FAILED: {e}")
            if "API_KEY_INVALID" in str(e) or "API key expired" in str(e):
                print("The API key appears to be invalid or expired.")
                print("Please check that you've copied the key correctly from Google AI Studio.")
            elif "429" in str(e):
                print("QUOTA EXCEEDED: You've used up your API quota for this period")
            return False
            
    except Exception as e:
        print(f"Configuration error: {e}")
        return False

if __name__ == "__main__":
    test_api_key()