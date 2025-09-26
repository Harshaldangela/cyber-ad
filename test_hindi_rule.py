from improved_rule_based_detector import ImprovedRuleBasedSpamDetector

detector = ImprovedRuleBasedSpamDetector()
prediction, confidence = detector.predict('बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें')
print('Prediction:', prediction)
print('Confidence:', confidence)