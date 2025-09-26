import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import google.generativeai as genai
import os
from datetime import datetime
import warnings
from config import get_gemini_api_key, get_app_config

# Suppress scikit-learn version warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# Get app configuration
config = get_app_config()

# Configure page
st.set_page_config(
    page_title=config['app_name'],
    page_icon=config['app_icon'],
    layout="wide"
)

# Initialize Porter Stemmer
ps = PorterStemmer()

def transform_text(text):
    """Transform text for model prediction"""
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = [i for i in text if i.isalnum()]
    text = [i for i in y if i not in stopwords.words('english') and i not in string.punctuation]
    text = [ps.stem(i) for i in text]
    return " ".join(text)

def generate_cyber_awareness_ad(spam_message, api_key):
    """Generate a cyber awareness ad using Gemini API based on the spam message"""
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Try different model names in order of preference
        model_names = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        model = None
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                # Test the model with a simple prompt
                test_response = model.generate_content("Hello")
                print(f"✅ Using model: {model_name}")
                break
            except Exception as model_error:
                print(f"❌ Model {model_name} not available: {model_error}")
                continue
        
        if model is None:
            return "Error: No compatible Gemini model found. Please check your API key and try again."
        
        # Create prompt for cyber awareness ad
        prompt = f"""
        Create a creative and engaging cyber awareness advertisement based on this spam message: "{spam_message}"
        
        The ad should:
        1. Be educational and informative about cybersecurity
        2. Be creative and attention-grabbing
        3. Include specific tips related to the type of spam shown
        4. Be suitable for social media or public awareness campaigns
        5. Include a catchy headline and clear call-to-action
        6. Be written in a friendly, non-technical tone
        
        Format the response as:
        **Headline:**
        [Creative headline]
        
        **Ad Content:**
        [Engaging ad content with cybersecurity tips]
        
        **Key Takeaway:**
        [One main security tip]
        
        **Call to Action:**
        [What readers should do]
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error generating cyber awareness ad: {str(e)}"

@st.cache_data(show_spinner=False)
def cached_translation(ad_text, language_name, api_key):
    """Cache wrapper for translate_ad to avoid duplicate API calls."""
    return translate_ad(ad_text, language_name, api_key)

def translate_ad(ad_text, target_language_name, api_key):
    """Translate the generated ad to a target language while preserving structure."""
    try:
        genai.configure(api_key=api_key)

        # Try a list of preferred models for translation
        model_names = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        model = None

        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                test_response = model.generate_content("Hello")
                break
            except Exception:
                continue

        if model is None:
            return "Error: No compatible Gemini model found for translation."

        prompt = f"""
        You are a professional translator. Translate the following content into {target_language_name}.
        Preserve the Markdown formatting and the original structure with these sections:
        - **Headline:**
        - **Ad Content:**
        - **Key Takeaway:**
        - **Call to Action:**

        Do not add new content. Keep the tone friendly and clear.

        ---
        SOURCE CONTENT:
        {ad_text}
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error translating ad: {str(e)}"

def load_models():
    """Load the trained model and vectorizer"""
    try:
        tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
        model = pickle.load(open('model.pkl', 'rb'))
        return tfidf, model
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None

# Main app
def main():
    # Header
    st.title("🛡️ GenAI Cyber Ad")
    st.markdown("---")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("🔑 Configuration")
        
        # Try to get API key from environment first
        env_api_key = get_gemini_api_key()
        default_api_key = env_api_key if env_api_key else ""
        
        api_key = st.text_input(
            "Enter your Gemini API Key (Preconfigured)",
            value=default_api_key,
            type="password",
            help="API key is preconfigured. You can override it here if needed."
        )
        
        if api_key:
            st.success("✅ API Key configured and ready!")
        else:
            st.warning("⚠️ API key not found. Please check configuration.")
        
        st.markdown("---")
        st.markdown("### How it works:")
        st.markdown("1. Enter an SMS message")
        st.markdown("2. Get spam classification")
        st.markdown("3. If spam detected, view cyber awareness ad")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This app uses machine learning to detect spam and generates educational cyber awareness content using Google's Gemini AI.")
    
    # Load models
    tfidf, model = load_models()
    if tfidf is None or model is None:
        st.error("Failed to load models. Please ensure model.pkl and vectorizer.pkl files are present.")
        return
    
    # Translation language options
    available_languages = [
        ("Hindi", "hi"), ("Marathi", "mr"), ("Bengali", "bn"), ("Telugu", "te"), ("Tamil", "ta"),
        ("Gujarati", "gu"), ("Kannada", "kn"), ("Malayalam", "ml"), ("Punjabi", "pa"), ("Urdu", "ur"),
        ("French", "fr"), ("Spanish", "es"), ("German", "de"), ("Arabic", "ar"), ("Chinese (Simplified)", "zh"),
        ("Japanese", "ja")
    ]

    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📱 Message Input")
        input_sms = st.text_area(
            "Enter the SMS message to classify:",
            height=150,
            placeholder="Paste your SMS message here..."
        )
        
        if st.button("🔍 Analyze Message", type="primary", use_container_width=True):
            if input_sms.strip():
                with st.spinner("Analyzing message..."):
                    # Transform and predict
                    transformed_sms = transform_text(input_sms)
                    vector_input = tfidf.transform([transformed_sms])
                    result = model.predict(vector_input)[0]
                    
                    # Store results in session state
                    st.session_state.result = result
                    st.session_state.input_sms = input_sms
                    st.session_state.timestamp = datetime.now()
                    
                    st.rerun()
            else:
                st.warning("Please enter a message to analyze.")
    
    with col2:
        st.header("📊 Analysis Results")
        
        if 'result' in st.session_state:
            result = st.session_state.result
            input_sms = st.session_state.input_sms
            
            # Display result with styling
            if result == 1:
                st.error("🚨 SPAM DETECTED")
                st.markdown("This message has been classified as **spam**.")
                
                # Show cyber awareness ad if API key is available
                if api_key:
                    st.markdown("---")
                    st.header("🛡️ Cyber Awareness Ad")
                    
                    with st.spinner("Generating cyber awareness content..."):
                        ad_content = generate_cyber_awareness_ad(input_sms, api_key)
                    
                    # Display the generated ad in a nice format
                    st.markdown("### Generated Cyber Awareness Content:")
                    st.markdown(ad_content)
                    
                    # Add download button for the ad
                    st.download_button(
                        label="📥 Download Ad Content",
                        data=ad_content,
                        file_name=f"cyber_awareness_ad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )

                    # Translation controls
                    st.markdown("---")
                    st.subheader("🌐 Translate this Ad")
                    selected_lang_names = st.multiselect(
                        "Select languages to translate into",
                        [name for name, _ in available_languages],
                        default=[]
                    )

                    if selected_lang_names:
                        with st.spinner("Translating..."):
                            translations = {}
                            for lang_name in selected_lang_names:
                                translated_text = cached_translation(ad_content, lang_name, api_key)
                                translations[lang_name] = translated_text

                        # Display translations
                        for lang_name in selected_lang_names:
                            st.markdown(f"### {lang_name}")
                            st.markdown(translations[lang_name])
                            st.download_button(
                                label=f"📥 Download {lang_name} Version",
                                data=translations[lang_name],
                                file_name=f"cyber_awareness_ad_{lang_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain",
                                key=f"download_{lang_name}"
                            )
                else:
                    st.info("💡 Enable Gemini API to generate cyber awareness ads for spam messages.")
                    
            else:
                st.success("✅ NOT SPAM")
                st.markdown("This message appears to be **legitimate**.")
            
            # Show analysis details
            st.markdown("---")
            st.markdown("### Analysis Details:")
            st.markdown(f"**Original Message:** {input_sms}")
            st.markdown(f"**Analysis Time:** {st.session_state.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            st.markdown(f"**Classification:** {'Spam' if result == 1 else 'Not Spam'}")
        else:
            st.info("👆 Enter a message and click 'Analyze Message' to get started.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>🛡️ Stay safe online! This tool helps identify spam and educates about cybersecurity.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
