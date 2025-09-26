from rule_based_detector import RuleBasedSpamDetector

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
    detector = RuleBasedSpamDetector()
    
    print("Testing Rule-Based Spam Detector")
    print("=" * 50)
    
    for i, message in enumerate(generic_spam_messages, 1):
        print(f"\nTest {i}:")
        print(f"Message: {message}")
        
        # Get features
        features = detector.extract_features(message)
        print(f"Features: {features}")
        
        # Get prediction
        prediction, confidence = detector.predict(message)
        label = "SPAM" if prediction == 1 else "HAM"
        
        print(f"Prediction: {label}")
        print(f"Confidence: {confidence:.4f}")
        
        # Check if this is a known spam message that should be classified as spam
        if prediction != 1:
            print("*** MISCLASSIFIED AS HAM - SHOULD BE SPAM ***")
        
        print("-" * 30)

if __name__ == "__main__":
    main()