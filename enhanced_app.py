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
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
import json
import base64

# Suppress scikit-learn version warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# Configure page
st.set_page_config(
    page_title="🛡️ Enhanced SMS Spam Classifier",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Porter Stemmer
ps = PorterStemmer()

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .dark-mode {
        background-color: #0e1117;
        color: white;
    }
    .card {
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        background-color: white;
    }
    .dark-mode .card {
        background-color: #1e1e1e;
        color: white;
    }
    .result-spam {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
    }
    .dark-mode .result-spam {
        background-color: #3a1a1a;
    }
    .result-not-spam {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
    }
    .dark-mode .result-not-spam {
        background-color: #1a3a1a;
    }
    .cyber-ad {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
    }
    .dark-mode .cyber-ad {
        background-color: #3a2a1a;
    }
    .header {
        color: #1976d2;
    }
    .dark-mode .header {
        color: #64b5f6;
    }
    .stButton>button {
        background-color: #1976d2;
        color: white;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1565c0;
    }
    .dark-mode .stButton>button {
        background-color: #64b5f6;
        color: #0e1117;
    }
    .dark-mode .stButton>button:hover {
        background-color: #90caf9;
    }
</style>
""", unsafe_allow_html=True)

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

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Generate a download link for a binary file"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

def init_session_state():
    """Initialize session state variables"""
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'stats' not in st.session_state:
        st.session_state.stats = {'spam': 0, 'not_spam': 0}

def toggle_dark_mode():
    """Toggle dark mode"""
    st.session_state.dark_mode = not st.session_state.dark_mode

def add_to_history(message, result, ad_content=None):
    """Add classification result to history"""
    st.session_state.history.append({
        'timestamp': datetime.now(),
        'message': message,
        'result': 'Spam' if result == 1 else 'Not Spam',
        'ad_content': ad_content
    })
    # Update stats
    if result == 1:
        st.session_state.stats['spam'] += 1
    else:
        st.session_state.stats['not_spam'] += 1

def display_stats():
    """Display statistics dashboard"""
    st.subheader("📊 Classification Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Messages", len(st.session_state.history))
    
    with col2:
        st.metric("Spam Detected", st.session_state.stats['spam'])
    
    with col3:
        st.metric("Legitimate", st.session_state.stats['not_spam'])
    
    if len(st.session_state.history) > 0:
        # Create a DataFrame for plotting
        df = pd.DataFrame(st.session_state.history)
        df['date'] = df['timestamp'].dt.date
        
        # Classification trend over time
        daily_counts = df.groupby(['date', 'result']).size().reset_index(name='count')
        
        fig = px.bar(daily_counts, x='date', y='count', color='result', 
                     title="Classification Trend Over Time",
                     color_discrete_map={'Spam': '#f44336', 'Not Spam': '#4caf50'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Pie chart of classifications
        result_counts = df['result'].value_counts()
        fig2 = px.pie(values=result_counts.values, names=result_counts.index, 
                      title="Spam vs Not Spam Distribution",
                      color_discrete_map={'Spam': '#f44336', 'Not Spam': '#4caf50'})
        st.plotly_chart(fig2, use_container_width=True)

# Main app
def main():
    # Initialize session state
    init_session_state()
    
    # Apply dark mode if enabled
    if st.session_state.dark_mode:
        st.markdown('<div class="dark-mode">', unsafe_allow_html=True)
    
    # Header
    st.title("🛡️ Enhanced SMS Spam Classifier")
    st.markdown("---")
    
    # Sidebar for API key and settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Dark mode toggle
        if st.button("🌓 Toggle Dark Mode"):
            toggle_dark_mode()
            st.rerun()
        
        st.markdown("---")
        
        # API Key configuration
        st.header("🔑 API Configuration")
        api_key = st.text_input(
            "Enter your Gemini API Key",
            value=st.session_state.api_key,
            type="password",
            help="Get your API key from Google AI Studio"
        )
        
        if api_key:
            st.session_state.api_key = api_key
            st.success("✅ API Key configured!")
        else:
            st.warning("⚠️ API key required for ad generation")
        
        st.markdown("---")
        st.markdown("### How it works:")
        st.markdown("1. Enter an SMS message")
        st.markdown("2. Get spam classification")
        st.markdown("3. If spam detected, view cyber awareness ad")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This enhanced app uses machine learning to detect spam and generates educational cyber awareness content using Google's Gemini AI.")
        
        # Display statistics in sidebar
        st.markdown("---")
        st.subheader("📈 Quick Stats")
        st.metric("Total Messages", len(st.session_state.history))
        st.metric("Spam Detected", st.session_state.stats['spam'])
        st.metric("Legitimate", st.session_state.stats['not_spam'])
    
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

    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📱 Classifier", "📊 Analytics", "🕒 History"])
    
    with tab1:
        # Main content area
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("📱 Message Input")
            input_sms = st.text_area(
                "Enter the SMS message to classify:",
                height=200,
                placeholder="Paste your SMS message here..."
            )
            
            # Real-time classification option
            real_time = st.checkbox("Enable real-time classification", value=False)
            
            if real_time and input_sms.strip():
                with st.spinner("Analyzing message..."):
                    # Transform and predict
                    transformed_sms = transform_text(input_sms)
                    vector_input = tfidf.transform([transformed_sms])
                    result = model.predict(vector_input)[0]
                    
                    # Display result immediately
                    if result == 1:
                        st.error("🚨 SPAM DETECTED")
                        st.markdown("This message has been classified as **spam**.")
                    else:
                        st.success("✅ NOT SPAM")
                        st.markdown("This message appears to be **legitimate**.")
            
            if st.button("🔍 Analyze Message", type="primary", use_container_width=True):
                if input_sms.strip():
                    with st.spinner("Analyzing message..."):
                        # Transform and predict
                        transformed_sms = transform_text(input_sms)
                        vector_input = tfidf.transform([transformed_sms])
                        result = model.predict(vector_input)[0]
                        
                        # Add to history
                        ad_content = None
                        if result == 1 and api_key:
                            ad_content = generate_cyber_awareness_ad(input_sms, api_key)
                        
                        add_to_history(input_sms, result, ad_content)
                        
                        # Display result
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
                        st.markdown(f"**Classification:** {'Spam' if result == 1 else 'Not Spam'}")
                else:
                    st.warning("Please enter a message to analyze.")
        
        with col2:
            st.header("ℹ️ Information")
            st.markdown("""
            ### About SMS Spam
            SMS spam (sometimes called "smishing") is a growing problem that can lead to:
            - Financial loss
            - Identity theft
            - Malware installation
            - Privacy breaches
            
            ### How to Identify Spam
            - Urgent or threatening language
            - Requests for personal information
            - Suspicious links or phone numbers
            - Unexpected prizes or offers
            - Poor grammar or spelling
            
            ### What This Tool Does
            This classifier uses machine learning to detect spam messages and provides educational content to help users understand cybersecurity risks.
            """)
    
    with tab2:
        st.header("📊 Analytics Dashboard")
        if len(st.session_state.history) > 0:
            display_stats()
        else:
            st.info("No classification history yet. Analyze some messages to see analytics.")
    
    with tab3:
        st.header("🕒 Classification History")
        if len(st.session_state.history) > 0:
            # Display history in reverse chronological order
            for i, item in enumerate(reversed(st.session_state.history)):
                with st.container():
                    st.markdown(f"**{item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}**")
                    st.markdown(f"**Message:** {item['message'][:100]}{'...' if len(item['message']) > 100 else ''}")
                    st.markdown(f"**Result:** {item['result']}")
                    if item['ad_content']:
                        with st.expander("View Generated Ad"):
                            st.markdown(item['ad_content'])
                    st.markdown("---")
        else:
            st.info("No classification history yet. Analyze some messages to populate history.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>🛡️ Enhanced SMS Spam Classifier with Cyber Awareness | Stay safe online!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
