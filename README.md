# SMS Spam Classifier with Cyber Awareness

## Overview

The SMS Spam Classifier is an advanced machine learning project that not only classifies SMS messages as spam or legitimate but also generates educational cyber awareness advertisements when spam is detected. The project uses Google's Gemini AI to create contextually relevant cybersecurity awareness content.

**Note**: This is the original version. For the complete enhanced version with React UI, Gmail extension, and improved models, see [COMPLETE_PROJECT_README.md](COMPLETE_PROJECT_README.md).

## Features

- **Spam Detection**: Machine learning-based SMS spam classification
- **Cyber Awareness Ads**: AI-generated educational content when spam is detected
- **Modern UI**: Beautiful Streamlit interface with real-time analysis
- **Downloadable Content**: Save generated cyber awareness ads for later use
- **Secure API Integration**: Safe handling of Gemini API keys

## Project Structure

- `app.py`: Enhanced Streamlit application with Gemini API integration
- `model_training.py`: Script to train the machine learning model and save it
- `requirements.txt`: List of Python dependencies including Google Generative AI
- `spam.csv`: Dataset used for training the model
- `vectorizer.pkl`: Pickled TF-IDF vectorizer used for text transformation
- `model.pkl`: Pickled trained machine learning model

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Manjesh501/sms-spam-classifier.git
   cd sms-spam-classifier
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Get Gemini API Key**

   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a new API key
   - Keep it secure for use in the application

## Usage

### Training the Model

Run the following command to train the model:

```bash
python model_training.py
```

This will generate the necessary files (`vectorizer.pkl` and `model.pkl`).

### Getting Your API Key

1. **Visit**: https://aistudio.google.com/app/apikey

2. **Create and copy your API key**

### Checking Available Models

If you encounter model errors, check which models are available:

```bash
python check_models.py
```

For specific Gemini 2.0 Flash testing:

```bash
python test_gemini_2.py
```

### Running the App

To start the Streamlit app, use:

```bash
streamlit run app.py
```

Open the local URL provided in your browser to interact with the application.

### Translating Generated Ads

After a spam message is detected and an ad is generated:
- Use the "Translate this Ad" multi-select to choose target languages
- Translations are generated via Gemini and cached to avoid repeat costs
- You can download each translated version as a .txt file

Supported examples: Hindi, Marathi, Bengali, Telugu, Tamil, Gujarati, Kannada, Malayalam, Punjabi, Urdu, French, Spanish, German, Arabic, Chinese (Simplified), Japanese.

## Backend API (FastAPI)

This project includes a small API so external clients (like the Gmail extension) can generate ads and translations without exposing your API key.

### Start the API

```bash
uvicorn api:app --reload --port 8000
```

### Endpoints

- POST `/generate-ad`
  - Body:
    ```json
    { "text": "<message to analyze>" }
    ```
  - Response: `{ "ad": "<generated ad markdown>" }`

- POST `/translate`
  - Body:
    ```json
    { "ad_text": "<generated ad markdown>", "languages": ["Hindi", "Spanish"] }
    ```
  - Response: `{ "translations": { "Hindi": "...", "Spanish": "..." } }`

## Gmail Integration (Chrome Extension)

You can inject a button into Gmail to generate cyber awareness ads for the currently opened email.

### Install (Load Unpacked)

1. Open Chrome → `chrome://extensions`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked" and select the `gmail-extension/` folder
4. Click the extension icon → "Cyber Ad Generator" → set Backend URL (e.g., `http://localhost:8000`)

### Use in Gmail

1. Open an email in `https://mail.google.com`
2. A "Generate Cyber Ad" button will appear above the message body
3. Click it to send the email text to the backend and render the ad below the message

Notes:
- The Chrome extension never sees your API key; it calls your local server
- Ensure the API (`uvicorn`) is running and reachable from the browser

### Using the Application

1. **Enter your Gemini API key** in the sidebar
2. **Paste an SMS message** in the input area
3. **Click "Analyze Message"** to get the classification
4. **If spam is detected**, view the generated cyber awareness ad
5. **Download the ad content** for use in awareness campaigns

## Example

**Input:** "Congratulations! You've won a prize. Click here to claim: bit.ly/fake-link"

**Output:** 
- Classification: Spam
- Generated Cyber Awareness Ad:
  - Headline: "Don't Let Fake Prizes Steal Your Data!"
  - Content: Educational content about phishing scams
  - Key Takeaway: Never click suspicious links
  - Call to Action: Report suspicious messages

**Input:** "Are we meeting tomorrow?"

**Output:** 
- Classification: Not Spam
- No ad generated (legitimate message)

## API Key Security

- The API key is stored only in the session and not saved permanently
- Use environment variables for production deployments
- Never commit API keys to version control

## Dependencies

- `streamlit`: Web application framework
- `google-generativeai`: Google's Generative AI library for Gemini integration
- `scikit-learn`: Machine learning library
- `nltk`: Natural language processing
- `pandas`, `numpy`: Data manipulation
- Other standard ML libraries

## Troubleshooting

### Common Issues

1. **Model loading errors:** Ensure all required files are present
2. **API key errors:** Verify your Gemini API key is correct
3. **Version conflicts:** Use the exact versions specified in requirements.txt
4. **Gemini model errors:** Run `python check_models.py` to see available models

### Model Errors

If you get "404 models/gemini-pro is not found" error:

1. Run the model checker: `python check_models.py`
2. The app will automatically try different model names
3. Make sure your API key has access to Gemini models

### API Key Issues

- Ensure your API key is valid and active
- Check that you have billing set up (if required)
- Verify the key has the necessary permissions

## Enhanced Version

For a complete solution with React UI, Gmail extension, and improved models, see [COMPLETE_PROJECT_README.md](COMPLETE_PROJECT_README.md).

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.