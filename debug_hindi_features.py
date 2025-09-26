from improved_rule_based_detector import ImprovedRuleBasedSpamDetector

detector = ImprovedRuleBasedSpamDetector()

# Test Hindi message
msg = 'बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें'

print(f"Testing message: {msg}")

# Extract features
features = detector.extract_features(msg)
print(f"Features: {features}")

# Get prediction
prediction, confidence = detector.predict(msg)
print(f"Prediction: {prediction}, Confidence: {confidence}")

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