import google.generativeai as genai
from config import get_gemini_api_key

# Configure the API
api_key = get_gemini_api_key()
if not api_key:
    print("No API key found")
    exit(1)

print(f"Using API key: {api_key[:10]}...")

genai.configure(api_key=api_key)

# Test specific models that are more likely to work
test_models = [
    "gemini-pro",
    "gemini-1.0-pro",
    "gemini-1.5-pro",
    "gemini-1.5-flash"
]

for model_name in test_models:
    try:
        print(f"Testing model: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello", request_options={"timeout": 10})
        print(f"  SUCCESS: {response.text[:50]}...")
        break
    except Exception as e:
        print(f"  FAILED: {e}")
else:
    print("No models worked!")