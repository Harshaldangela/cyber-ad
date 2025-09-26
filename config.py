import os
from typing import Optional

def get_gemini_api_key() -> Optional[str]:
    """
    Get Gemini API key from environment variable or return preconfigured key
    """
    # First try environment variable
    env_key = os.getenv('GEMINI_API_KEY')
    if env_key:
        return env_key
    
    # Return preconfigured API key
    return "AIzaSyAkVR2FisWx59ifqv2pG3r3D1jq4YgPHEA"

def get_app_config():
    """
    Get application configuration
    """
    return {
        'app_name': 'SMS Spam Classifier with Cyber Awareness',
        'app_icon': '🛡️',
        'max_message_length': 1000,
        'supported_languages': ['english'],
        'model_files': ['model.pkl', 'vectorizer.pkl'],
        'data_file': 'spam.csv'
    }

# Example usage:
# To set your API key as an environment variable:
# export GEMINI_API_KEY="your_api_key_here"
# 
# Or on Windows:
# set GEMINI_API_KEY=your_api_key_here