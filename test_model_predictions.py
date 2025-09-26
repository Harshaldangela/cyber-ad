import pickle
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Initialize stemmer
ps = PorterStemmer()

def advanced_text_preprocessing(text):
    """Advanced text preprocessing for better feature extraction"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove phone numbers
    text = re.sub(r'\d{3,}', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove punctuation and non-alphabetic tokens
    tokens = [token for token in tokens if token.isalpha() and len(token) > 1]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Stemming
    tokens = [ps.stem(token) for token in tokens]
    
    return " ".join(tokens)

def main():
    # Load the robust model and vectorizer
    try:
        tfidf = pickle.load(open('robust_vectorizer.pkl', 'rb'))
        clf = pickle.load(open('robust_model.pkl', 'rb'))
        print("Robust model loaded successfully!")
        print(f"Model type: {type(clf)}")
    except Exception as e:
        print(f"Error loading robust model: {e}")
        return
    
    # Test messages
    test_messages = [
        "Congratulations! You've won a $1000 gift card!",
        "Hey, are we still meeting for lunch tomorrow?",
        "Your account has been suspended. Verify here: http://bank-verify.com",
        "बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें"
    ]
    
    print("\nTesting model predictions:")
    print("=" * 50)
    
    for msg in test_messages:
        # Preprocess the message
        transformed = advanced_text_preprocessing(msg)
        print(f"\nOriginal: {msg}")
        print(f"Preprocessed: {transformed}")
        
        # Transform and predict
        vec = tfidf.transform([transformed])
        prediction = clf.predict(vec)[0]
        prob = clf.predict_proba(vec)[0]
        
        label = "SPAM" if prediction == 1 else "NOT SPAM"
        spam_prob = prob[1]  # Probability of being spam
        
        print(f"Prediction: {label}")
        print(f"Spam Probability: {spam_prob:.6f}")
        print(f"Not Spam Probability: {prob[0]:.6f}")

if __name__ == "__main__":
    main()