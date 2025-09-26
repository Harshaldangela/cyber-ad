from improved_rule_based_detector import ImprovedRuleBasedSpamDetector

def main():
    detector = ImprovedRuleBasedSpamDetector()
    
    # Test the specific message
    msg = "Make money fast! Double your investment in 24 hours. Click here: http://invest-now.com Limited time offer"
    
    print(f"Testing message: {msg}")
    
    # Get prediction
    prediction, confidence = detector.predict(msg)
    label = "SPAM" if prediction == 1 else "NOT SPAM"
    print(f"Rule-based Prediction: {label}, Confidence: {confidence}")
    
    # Check what keywords are being matched
    text_lower = msg.lower()
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