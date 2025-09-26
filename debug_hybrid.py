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

# Generic spam messages to test
generic_spam_messages = [
    # English messages
    "Congratulations! You've won a $1000 gift card! Click here to claim: http://bit.ly/claim-now Reply within 24 hours or prize expires.",
    "Your account has been suspended. Verify here: http://bank-verify.com Click now or account will be locked.",
    "Your package delivery failed. Reschedule here: http://delivery-reschedule.com Click to arrange pickup.",
    "Work from home opportunity! $2000/month guaranteed income. Apply now: http://job-apply.com No experience needed.",
    "Your computer has viruses. Call now: 1-800-555-0123 Immediate assistance required.",
    "Hi, I need you to buy gift cards urgently. Send codes ASAP. Will reimburse tomorrow.",
    "Hi! I think we know each other. Check my profile: http://profile-view.com Let's connect!",
    "Hi there! You seem interesting. I'm new to the area. Want to chat? Text me: 555-0123",
    "Make money fast! Double your investment in 24 hours. Click here: http://invest-now.com Limited time offer.",
    "Take this quick survey! Win $500 instantly. Click here: http://survey-win.com Only 2 minutes!",
    
    # Hindi messages
    "बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें'",
    "बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें' http://bank-verify.com",
    
    # Additional messages from earlier
    "Congratulations! You've won ₹10 lakh in the online lottery. To claim your prize, send your bank account details and pay a processing fee.",
    "Your mobile number has been selected for a ₹25 lakh international WhatsApp lottery. Contact this number to claim your prize.",
    "Lucky Winner! You've won ₹10,00,000. Click the link and enter your details to receive the amount."
]

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
    
    print("Testing Hybrid Spam Detection")
    print("=" * 50)
    
    for i, message in enumerate(generic_spam_messages, 1):
        print(f"\nTest {i}:")
        print(f"Message: {message}")
        
        # Get ML model prediction if available
        ml_prediction = None
        ml_confidence = 0.0
        
        if _tfidf is not None and _clf is not None:
            try:
                # Preprocess the text
                transformed = advanced_text_preprocessing(message)
                print(f"Preprocessed text: {transformed}")
                
                # Transform and predict
                vec = _tfidf.transform([transformed])
                ml_prediction = _clf.predict(vec)[0]
                prob = _clf.predict_proba(vec)[0]
                ml_confidence = max(prob)
                print(f"ML Prediction: {ml_prediction}, Confidence: {ml_confidence:.4f}")
            except Exception as e:
                print(f"ML model prediction error: {e}")
        
        # Get rule-based prediction
        rule_prediction, rule_confidence = _rule_detector.predict(message)
        print(f"Rule-based Prediction: {rule_prediction}, Confidence: {rule_confidence:.4f}")
        
        # Combine predictions (simplified version of hybrid_spam_detection)
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
        
        label = "SPAM" if final_prediction == 1 else "HAM"
        print(f"Hybrid Prediction: {label}, Confidence: {combined_confidence:.4f}")
        
        # Check if this is a known spam message that should be classified as spam
        if final_prediction != 1:
            print("*** MISCLASSIFIED AS HAM - SHOULD BE SPAM ***")
        
        print("-" * 30)

if __name__ == "__main__":
    main()