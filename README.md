# SMS Spam Classifier with Cyber Awareness

## Overview

The SMS Spam Classifier is an advanced machine learning project that not only classifies SMS messages as spam or legitimate but also generates educational cyber awareness advertisements when spam is detected. The project uses Google's Gemini AI to create contextually relevant cybersecurity awareness content.

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
   ./venv/Scripts/Activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Get Gemini API Key**

   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
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

1. **Run the helper script:**
   ```bash
   python get_api_key.py
   ```
   This will open Google AI Studio in your browser.

2. **Or manually visit:** https://makersuite.google.com/app/apikey

3. **Create and copy your API key**

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

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
