# SMS Spam Classifier with Cyber Awareness - Complete Project

## Overview

This is a comprehensive SMS Spam Classifier project that not only classifies SMS messages as spam or legitimate but also generates educational cyber awareness advertisements when spam is detected. The project includes multiple interfaces:

1. **Streamlit UI** - Original interface
2. **React Web Application** - Modern web interface with enhanced features
3. **Gmail Chrome Extension** - Browser extension for analyzing emails directly in Gmail
4. **FastAPI Backend** - REST API for all classification and ad generation services

The project uses advanced machine learning models and Google's Gemini AI to create contextually relevant cybersecurity awareness content.

## Features

### Core Classification Features
- **Advanced ML Model**: Logistic Regression with TF-IDF and n-grams for 97.7% accuracy
- **Hybrid Detection**: Combines ML model with rule-based detection for better accuracy
- **Confidence Scoring**: Provides confidence levels for each classification
- **Multi-language Support**: Supports classification of messages in multiple languages

### Cyber Awareness Features
- **AI-generated Ads**: Creates educational cyber awareness content when spam is detected
- **Multi-language Translation**: Translates ads to 15+ languages
- **Downloadable Content**: Save generated ads and translations as text files

### Interface Options
- **Streamlit UI**: Simple and intuitive original interface
- **React Web App**: Modern, responsive web application with dark/light mode
- **Gmail Extension**: Chrome extension for analyzing emails directly in Gmail
- **REST API**: Backend API for integration with other applications

### Technical Features
- **Real-time Analysis**: Instant classification and ad generation
- **Secure API Integration**: Safe handling of Gemini API keys
- **Error Handling**: Graceful handling of API quotas and model access issues
- **Extensible Architecture**: Modular design for easy enhancements

## Project Structure

```
sms-spam-classifier/
├── gmail-extension/              # Chrome extension for Gmail integration
│   ├── background.js            # Background service worker
│   ├── content.js               # Content script for Gmail DOM manipulation
│   ├── manifest.json            # Extension manifest
│   ├── popup.html               # Extension popup UI
│   ├── popup.js                 # Extension popup functionality
│   └── styles.css               # Extension styling
├── react-ui/                    # React web application
│   ├── public/                  # Public assets
│   ├── src/                     # Source code
│   │   ├── components/          # React components
│   │   ├── App.js               # Main application component
│   │   └── index.js             # Entry point
│   └── package.json             # React dependencies
├── api.py                       # Original FastAPI backend
├── enhanced_api.py              # Enhanced FastAPI backend with hybrid detection
├── app.py                       # Original Streamlit app
├── enhanced_app.py              # Enhanced Streamlit app
├── model_training.py            # Original model training script
├── improved_model_training.py   # Improved model training with better features
├── robust_model_training.py     # Robust model training with advanced preprocessing
├── rule_based_detector.py       # Basic rule-based spam detection
├── improved_rule_based_detector.py  # Enhanced rule-based detection
├── config.py                    # Configuration management
├── requirements.txt             # Python dependencies
├── enhanced_requirements.txt    # Enhanced Python dependencies
├── spam.csv                     # Training dataset
├── vectorizer.pkl               # TF-IDF vectorizer
├── model.pkl                    # Trained ML model
├── improved_vectorizer.pkl      # Improved TF-IDF vectorizer
├── improved_model.pkl           # Improved ML model
├── robust_vectorizer.pkl        # Robust TF-IDF vectorizer
├── robust_model.pkl             # Robust ML model
└── start_server.py              # Server startup script
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js and npm (for React UI)
- Google Gemini API key (free tier available)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd sms-spam-classifier-main
```

### 2. Set Up Python Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r enhanced_requirements.txt
```

### 4. Install React Dependencies

```bash
cd react-ui
npm install
cd ..
```

### 5. Get Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API key" or "Create API key"
4. Copy the generated API key
5. Add it to the `.env` file or [config.py](file:///C:/Users/Harsh/Downloads/sms-spam-classifier-main/sms-spam-classifier-main/config.py):

```env
GEMINI_API_KEY="your-api-key-here"
```

## Training Models

### Robust Model (Recommended)
```bash
python robust_model_training.py
```

This creates `robust_vectorizer.pkl` and `robust_model.pkl` with:
- Advanced text preprocessing
- TF-IDF with n-grams (unigrams, bigrams, trigrams)
- Logistic Regression classifier
- Enhanced feature engineering

### Improved Model
```bash
python improved_model_training.py
```

### Original Model
```bash
python model_training.py
```

## Running the Applications

### 1. Start the Backend API Server

The backend API provides all classification and ad generation services:

```bash
python start_server.py
```

The server will start on `http://localhost:8007`

#### API Endpoints

- **POST `/analyze`**
  - Analyze a message and classify it as spam/not spam
  - If spam, generates a cyber awareness ad
  - Request:
    ```json
    {
      "text": "Make money fast! Click here: http://example.com",
      "languages": ["Hindi", "Spanish"]  // Optional translations
    }
    ```
  - Response:
    ```json
    {
      "classification": "spam",
      "confidence": 0.95,
      "ad": "Headline: Don't Get Hooked! 🎣\n...",
      "translations": {
        "Hindi": "...",
        "Spanish": "..."
      }
    }
    ```

- **POST `/generate-ad`**
  - Generate a cyber awareness ad from text
  - Request:
    ```json
    {
      "text": "Make money fast! Click here: http://example.com"
    }
    ```
  - Response:
    ```json
    {
      "ad": "Headline: Don't Get Hooked! 🎣\n..."
    }
    ```

- **POST `/translate`**
  - Translate an ad to multiple languages
  - Request:
    ```json
    {
      "ad_text": "Headline: Don't Get Hooked! 🎣\n...",
      "languages": ["Hindi", "Spanish"]
    }
    ```
  - Response:
    ```json
    {
      "translations": {
        "Hindi": "...",
        "Spanish": "..."
      }
    }
    ```

- **GET `/health`**
  - Check server health and loaded models
  - Response:
    ```json
    {
      "status": "healthy",
      "model_loaded": true,
      "rule_detector_loaded": true
    }
    ```

### 2. Run the React Web Application

In a new terminal:

```bash
cd react-ui
npm start
```

The React app will start on `http://localhost:3000` (or next available port)

#### React App Features

- **Modern UI**: Clean, responsive design with dark/light mode
- **Real-time Classification**: Instant analysis of SMS messages
- **Confidence Visualization**: Visual representation of classification confidence
- **Cyber Awareness Ads**: Generated ads with download capability
- **Multi-language Translation**: Translate ads to various languages
- **Classification History**: Track previous classifications
- **Model Information**: View details about the ML model

### 3. Run the Streamlit Application

```bash
streamlit run enhanced_app.py
```

The Streamlit app will start on `http://localhost:8501`

### 4. Install and Use the Gmail Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `gmail-extension` folder
5. Click the extension icon and set the Backend URL to `http://localhost:8007`
6. Open Gmail and view any email - you'll see an "Analyze & Generate" button

## Supported Languages for Translation

The system can translate generated ads to the following languages:
- Hindi, Marathi, Bengali, Telugu, Tamil, Gujarati, Kannada, Malayalam, Punjabi, Urdu
- French, Spanish, German, Arabic
- Chinese (Simplified), Japanese

## Model Performance

### Robust Model (Recommended)
- **Accuracy**: ~97.7%
- **Precision**: ~95.0%
- **Recall**: ~86.3%
- **F1-Score**: ~90.4%

### Key Improvements
- Advanced text preprocessing (URL/email/phone number removal)
- TF-IDF with n-grams (unigrams, bigrams, trigrams)
- Logistic Regression classifier with optimized parameters
- Confidence scoring for each prediction
- Hybrid approach combining ML and rule-based detection
- Better handling of edge cases and Hindi spam messages

## API Key Security

- The API key is stored in [config.py](file:///C:/Users/Harsh/Downloads/sms-spam-classifier-main/sms-spam-classifier-main/config.py) or [.env](file:///C:/Users/Harsh/Downloads/sms-spam-classifier-main/sms-spam-classifier-main/.env) file
- For production deployments, use environment variables
- Never commit API keys to version control
- The Chrome extension never sees your API key; it calls your local server

## Troubleshooting

### Common Issues

1. **API Quota Exceeded (429 Error)**
   - Solution: Get your own Google AI API key with higher quotas
   - The system gracefully handles this by continuing classification without ad generation

2. **Model Not Found (404 Error)**
   - Solution: The system automatically tries different model names
   - Make sure your API key has access to Gemini models

3. **Server Not Starting**
   - Check that port 8007 is available
   - Ensure all Python dependencies are installed

4. **React App Not Starting**
   - Ensure Node.js and npm are installed
   - Run `npm install` in the react-ui directory

5. **Extension Not Working**
   - Verify the backend URL is set to `http://localhost:8007`
   - Ensure the API server is running
   - Check Chrome's extension console for errors

### Testing the System

You can test the complete system with these example messages:

**Spam Message:**
```
Make money fast! Double your investment in 24 hours. Click here: http://invest-now.com Limited time offer.
```

**Phishing Message:**
```
Urgent: Your account has been compromised. Click here to verify: http://fake-bank.com/verify
```

**Normal Message:**
```
Hi, how are you doing today? Let's meet for coffee tomorrow.
```

**Hindi Spam Message:**
```
बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें http://bank-verify.com
```

## Architecture

### Backend (FastAPI)
- Handles all ML model inference
- Manages Gemini API interactions
- Provides REST endpoints for all clients
- Implements hybrid detection approach
- Handles error cases gracefully

### Frontend (React)
- Modern, responsive UI
- Real-time classification
- Dark/light mode support
- History tracking
- Multi-language translation

### Gmail Extension
- Content script injects button into Gmail
- Background script handles API communication
- Popup for settings configuration
- Secure messaging to backend

## Contributing

Feel free to submit issues and enhancement requests!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is open source and available under the MIT License.