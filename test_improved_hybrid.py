import pickle
import sys
import os
from rule_based_detector import RuleBasedSpamDetector

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def advanced_text_preprocessing(text: str) -> str:
    """Advanced text preprocessing for better feature extraction"""
    import re
    import string
    from nltk.corpus import stopwords
    import nltk
    from nltk.stem.porter import PorterStemmer
    
    _ps = PorterStemmer()
    
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
    tokens = nltk.word_tokenize(text)
    
    # Remove punctuation and non-alphabetic tokens
    tokens = [token for token in tokens if token.isalpha() and len(token) > 1]
    
    # Remove stopwords
    try:
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
    except:
        # Fallback if stopwords not available
        pass
    
    # Stemming
    tokens = [_ps.stem(token) for token in tokens]
    
    return " ".join(tokens)

def improved_hybrid_spam_detection(text: str, _tfidf, _clf, _rule_detector):
    """
    Improved hybrid spam detection combining ML model and rule-based approach
    Returns: (prediction, confidence) where prediction is 1 for spam, 0 for ham
    """
    # Get ML model prediction if available
    ml_prediction = None
    ml_confidence = 0.0
    
    if _tfidf is not None and _clf is not None:
        try:
            # Preprocess the text
            transformed = advanced_text_preprocessing(text)
            
            # Transform and predict
            vec = _tfidf.transform([transformed])
            ml_prediction = _clf.predict(vec)[0]
            prob = _clf.predict_proba(vec)[0]
            ml_confidence = max(prob)
        except Exception as e:
            print(f"ML model prediction error: {e}")
    
    # Get rule-based prediction
    rule_prediction, rule_confidence = _rule_detector.predict(text)
    
    print(f"ML Prediction: {ml_prediction}, Confidence: {ml_confidence}")
    print(f"Rule Prediction: {rule_prediction}, Confidence: {rule_confidence}")
    
    # Improved combination logic
    if ml_prediction is not None:
        # If both models agree, use higher confidence
        if ml_prediction == rule_prediction:
            combined_confidence = max(ml_confidence, rule_confidence)
            final_prediction = ml_prediction
        else:
            # If they disagree, we need to be more careful
            # Rule-based detector is more reliable for known spam patterns
            # Give higher weight to rule-based for high confidence cases
            
            # Check if this is a known spam pattern that the rule detector recognizes
            if rule_confidence > 0.5:  # Moderate confidence from rules
                # If rule-based has moderate to high confidence, trust it more
                final_prediction = rule_prediction
                # Boost confidence a bit since we trust the rules
                combined_confidence = min(1.0, rule_confidence + 0.1)
            elif ml_confidence > 0.9:  # Very high confidence from ML
                # If ML is very confident, trust it
                final_prediction = ml_prediction
                combined_confidence = ml_confidence
            else:
                # Default to rule-based when in doubt, as it's more reliable for spam detection
                final_prediction = rule_prediction
                combined_confidence = rule_confidence
    else:
        # Fallback to rule-based only
        final_prediction = rule_prediction
        combined_confidence = rule_confidence
    
    return int(final_prediction), float(combined_confidence)

def main():
    # Load the robust model and vectorizer
    try:
        _tfidf = pickle.load(open('robust_vectorizer.pkl', 'rb'))
        _clf = pickle.load(open('robust_model.pkl', 'rb'))
        print("Robust model loaded successfully!")
    except Exception as e:
        print(f"Error loading robust model: {e}")
        _tfidf = None
        _clf = None
    
    # Initialize rule-based detector
    _rule_detector = RuleBasedSpamDetector()
    
    # Test messages
    test_messages = [
        "Congratulations! You've won a $1000 gift card!",
        "Your account has been suspended. Verify here: http://bank-verify.com",
        "बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें"
    ]
    
    for msg in test_messages:
        print(f"\nTesting message: {msg}")
        
        # Get improved hybrid prediction
        prediction, confidence = improved_hybrid_spam_detection(msg, _tfidf, _clf, _rule_detector)
        label = "SPAM" if prediction == 1 else "NOT SPAM"
        print(f"Improved Hybrid Prediction: {label}, Confidence: {confidence}")

if __name__ == "__main__":
    main()