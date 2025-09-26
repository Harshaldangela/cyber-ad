import google.generativeai as genai
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the config module
from config import get_gemini_api_key

def simple_test():
    # Get the API key
    api_key = get_gemini_api_key()
    print(f"API Key (first 15 chars): {api_key[:15] if api_key else 'None'}")
    
    if not api_key:
        print("No API key found!")
        return False
        
    try:
        genai.configure(api_key=api_key)
        print("Gemini API configured")
        
        # Try the simplest model first
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("What is 2+2? Answer in one word.")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        # Try to identify the specific issue
        error_str = str(e).lower()
        if "api_key_invalid" in error_str or "api key expired" in error_str:
            print("The API key is invalid or expired.")
            print("Please get a new key from https://aistudio.google.com/")
        elif "429" in error_str:
            print("Rate limit exceeded. Try again later.")
        elif "404" in error_str:
            print("Model not found. Trying alternative models...")
        return False

if __name__ == "__main__":
    simple_test()