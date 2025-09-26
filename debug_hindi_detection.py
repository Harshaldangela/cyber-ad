from rule_based_detector import RuleBasedSpamDetector

def main():
    detector = RuleBasedSpamDetector()
    
    # Test Hindi message
    hindi_message = "बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें"
    
    print(f"Testing Hindi message: {hindi_message}")
    
    # Extract features
    features = detector.extract_features(hindi_message)
    print(f"Features: {features}")
    
    # Get prediction
    prediction, confidence = detector.predict(hindi_message)
    label = "SPAM" if prediction == 1 else "NOT SPAM"
    print(f"Prediction: {label}, Confidence: {confidence}")
    
    # Check what keywords are being matched
    text_lower = hindi_message.lower()
    print("\nKeyword matches:")
    for keyword in detector.spam_keywords:
        count = text_lower.count(keyword)
        if count > 0:
            print(f"  '{keyword}': {count} matches")
    
    # Check what patterns are being matched
    import re
    print("\nPattern matches:")
    for pattern in detector.suspicious_patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            print(f"  '{pattern}': {matches}")
    
    # Check high confidence patterns
    print("\nHigh confidence pattern matches:")
    for pattern in detector.high_confidence_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            print(f"  '{pattern}': MATCH")

if __name__ == "__main__":
    main()