# Enhanced SMS Spam Classifier with Cyber Awareness

## Overview

The Enhanced SMS Spam Classifier is an advanced machine learning project that not only classifies SMS messages as spam or legitimate but also generates educational cyber awareness advertisements when spam is detected. This enhanced version includes a modern UI with analytics dashboard, dark mode, and improved user experience.

**Note**: This is the enhanced Streamlit version. For the complete solution with React UI, Gmail extension, and all features, see [COMPLETE_PROJECT_README.md](COMPLETE_PROJECT_README.md).

The project uses Google's Gemini AI to create contextually relevant cybersecurity awareness content.

## Enhanced Features

- **Enhanced UI/UX**: Modern interface with dark/light mode toggle
- **Analytics Dashboard**: Visualize spam detection statistics and trends
- **Classification History**: Track and review previous classifications
- **Real-time Classification**: Option for real-time message analysis
- **Improved Responsive Design**: Better experience on all devices
- **Enhanced Information Section**: Educational content about SMS spam
- **Better Organization**: Tab-based navigation for different features

## Project Structure

- `enhanced_app.py`: Enhanced Streamlit application with all new features
- `app.py`: Original Streamlit application
- `model_training.py`: Script to train the machine learning model and save it
- `enhanced_requirements.txt`: Updated dependencies for enhanced features
- `requirements.txt`: Original dependencies
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

3. **Install Enhanced Dependencies**

   ```bash
   pip install -r enhanced_requirements.txt
   ```

4. **Get Gemini API Key**

   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a new API key
   - Keep it secure for use in the application

## Usage

### Training the Model

If you need to retrain the model:

```bash
python model_training.py
```

This will generate the necessary files (`vectorizer.pkl` and `model.pkl`).

### Running the Enhanced App

To start the enhanced Streamlit app, use:

```bash
streamlit run enhanced_app.py
```

Open the local URL provided in your browser to interact with the enhanced application.

### Features in the Enhanced App

1. **Dark/Light Mode Toggle**: Switch between themes based on your preference
2. **Analytics Dashboard**: View statistics and trends of your classifications
3. **History Tab**: Review all previous classifications
4. **Real-time Classification**: Enable real-time analysis as you type
5. **Information Section**: Learn about SMS spam and how to identify it

### Using the Application

1. **Enter your Gemini API key** in the sidebar
2. **Paste an SMS message** in the input area
3. **Click "Analyze Message"** to get the classification
4. **If spam is detected**, view the generated cyber awareness ad
5. **Download the ad content** for use in awareness campaigns
6. **Switch to Analytics tab** to view statistics
7. **Switch to History tab** to review previous classifications

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
- `plotly`: Interactive charts and graphs
- `google-generativeai`: Google's Generative AI library for Gemini integration
- `scikit-learn`: Machine learning library
- `nltk`: Natural language processing
- `pandas`, `numpy`: Data manipulation
- Other standard ML libraries

## Troubleshooting

### Common Issues

1. **Model loading errors:** Ensure all required files are present
2. **API key errors:** Verify your Gemini API key is correct
3. **Version conflicts:** Use the exact versions specified in enhanced_requirements.txt
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

## Complete Solution

For the full solution including React UI, Gmail extension, and improved ML models, see [COMPLETE_PROJECT_README.md](COMPLETE_PROJECT_README.md).

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.