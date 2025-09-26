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

def hybrid_spam_detection(text: str, _tfidf, _clf, _rule_detector):
    """
    Hybrid spam detection combining ML model and rule-based approach
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
    
    # Combine predictions
    if ml_prediction is not None:
        # If both models agree, use higher confidence
        if ml_prediction == rule_prediction:
            combined_confidence = max(ml_confidence, rule_confidence)
            final_prediction = ml_prediction
        else:
            # If they disagree, use the one with higher confidence
            # But give slight preference to rule-based for high confidence cases
            if rule_confidence > 0.8:  # High confidence from rules
                final_prediction = rule_prediction
                combined_confidence = rule_confidence
            elif ml_confidence > 0.8:  # High confidence from ML
                final_prediction = ml_prediction
                combined_confidence = ml_confidence
            else:
                # For lower confidence cases, use ML model
                final_prediction = ml_prediction
                combined_confidence = ml_confidence
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
    
    # Test message
    test_message = "Congratulations! You've won a $1000 gift card!"
    print(f"Testing message: {test_message}")
    
    # Get hybrid prediction
    prediction, confidence = hybrid_spam_detection(test_message, _tfidf, _clf, _rule_detector)
    label = "SPAM" if prediction == 1 else "NOT SPAM"
    print(f"Hybrid Prediction: {label}, Confidence: {confidence}")

if __name__ == "__main__":
    main()