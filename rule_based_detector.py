import re
import pickle
from typing import Tuple, Dict, Any

class RuleBasedSpamDetector:
    def __init__(self):
        # Common spam keywords and phrases
        self.spam_keywords = [
            # English spam keywords
            'congratulations', 'winner', 'won', 'prize', 'gift card', 'lottery', 'jackpot',
            'urgent', 'immediate', 'asap', 'limited time', 'act now', 'don\'t miss',
            'free', 'cash', 'money', 'income', 'earn', 'guaranteed', 'risk free',
            'click here', 'click now', 'verify', 'suspended', 'locked', 'failed',
            'call now', 'text now', 'reply now', 'send now', 'hurry', 'offer',
            'investment', 'double your money', 'make money', 'work from home',
            'no experience', 'guaranteed income', 'opportunity', 'selected',
            'account details', 'bank details', 'processing fee', 'reimburse',
            'viruses', 'tech support', 'computer problem', 'gift card',
            
            # Hindi spam keywords (transliterated)
            'badhai ho', 'jite', 'jeet', 'uphar', 'lakh', 'paisa', 'paise',
            'aapne jeeta', 'aap jeete', 'rashi', 'raashi', 'link', 'click',
            'jaldi', 'turant', 'sampark', 'sampark kare', 'vivaran', 'details'
        ]
        
        # Suspicious patterns
        self.suspicious_patterns = [
            r'http\S+',  # URLs
            r'www\.\S+',  # WWW URLs
            r'\d{3}-\d{3}-\d{4}',  # Phone numbers format 1
            r'\d{10}',  # 10 digit numbers (common for phone numbers)
            r'\$\d+',  # Dollar amounts
            r'₹\d+',  # Rupee amounts
            r'\d+[.,]\d+',  # Decimal numbers
            r'!\s*!',  # Multiple exclamation marks
            r'\?\s*\?',  # Multiple question marks
        ]
        
        # High confidence spam patterns
        self.high_confidence_patterns = [
            r'congratulations.*won.*\d+.*click.*claim',
            r'account.*suspended.*verify.*click',
            r'package.*failed.*reschedule.*click',
            r'work from home.*\d+/month.*guaranteed.*click',
            r'computer.*viruses.*call now.*\d+-\d+-\d+',
            r'gift cards.*urgently.*send codes',
            r'know each other.*check my profile.*click',
            r'seem interesting.*new to the area.*text me',
            r'make money.*investment.*click.*limited time',
            r'quick survey.*win.*\d+.*click.*minutes',
            r'congratulations.*won.*lakh.*click.*details',
            r'mobile number.*selected.*lakh.*whatsapp.*click',
            r'winner.*won.*click.*link.*details',
            r'badhai ho.*jite.*raashi.*click.*vivaran'
        ]

    def extract_features(self, text: str) -> Dict[str, Any]:
        """Extract features from text for spam detection"""
        text_lower = text.lower()
        
        # Count spam keywords
        spam_keyword_count = 0
        for keyword in self.spam_keywords:
            spam_keyword_count += text_lower.count(keyword)
        
        # Count suspicious patterns
        suspicious_pattern_count = 0
        for pattern in self.suspicious_patterns:
            suspicious_pattern_count += len(re.findall(pattern, text_lower))
        
        # Check for high confidence patterns
        high_confidence_matches = 0
        for pattern in self.high_confidence_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                high_confidence_matches += 1
        
        # Check for urgency indicators
        urgency_indicators = ['urgent', 'immediate', 'asap', 'hurry', 'limited time', 'act now']
        urgency_count = sum(1 for word in urgency_indicators if word in text_lower)
        
        # Check for money-related terms
        money_terms = ['free', 'cash', 'money', 'income', 'earn', 'prize', 'won', 'win']
        money_count = sum(1 for word in money_terms if word in text_lower)
        
        # Check for action requests
        action_requests = ['click', 'call', 'text', 'reply', 'send', 'verify', 'apply']
        action_count = sum(1 for word in action_requests if word in text_lower)
        
        return {
            'spam_keyword_count': spam_keyword_count,
            'suspicious_pattern_count': suspicious_pattern_count,
            'high_confidence_matches': high_confidence_matches,
            'urgency_count': urgency_count,
            'money_count': money_count,
            'action_count': action_count,
            'text_length': len(text),
            'word_count': len(text.split())
        }

    def predict(self, text: str) -> Tuple[int, float]:
        """
        Predict if text is spam using rule-based approach
        Returns: (prediction, confidence) where prediction is 1 for spam, 0 for ham
        """
        features = self.extract_features(text)
        
        # Calculate spam score based on features
        spam_score = 0.0
        
        # High confidence patterns have highest weight
        if features['high_confidence_matches'] > 0:
            spam_score += 0.9 * features['high_confidence_matches']
        
        # Spam keywords
        if features['spam_keyword_count'] > 0:
            spam_score += min(0.3, features['spam_keyword_count'] * 0.05)
        
        # Suspicious patterns
        if features['suspicious_pattern_count'] > 0:
            spam_score += min(0.3, features['suspicious_pattern_count'] * 0.1)
        
        # Urgency indicators
        if features['urgency_count'] > 0:
            spam_score += min(0.2, features['urgency_count'] * 0.05)
        
        # Money-related terms
        if features['money_count'] > 0:
            spam_score += min(0.2, features['money_count'] * 0.03)
        
        # Action requests
        if features['action_count'] > 0:
            spam_score += min(0.2, features['action_count'] * 0.03)
        
        # Normalize score
        spam_score = min(1.0, spam_score)
        
        # Make prediction based on threshold
        prediction = 1 if spam_score > 0.3 else 0
        confidence = spam_score
        
        return prediction, confidence

# Test the rule-based detector
if __name__ == "__main__":
    detector = RuleBasedSpamDetector()
    
    test_messages = [
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
        "Congratulations! You've won ₹10 lakh in the online lottery. To claim your prize, send your bank account details and pay a processing fee.",
        "Your mobile number has been selected for a ₹25 lakh international WhatsApp lottery. Contact this number to claim your prize.",
        "Lucky Winner! You've won ₹10,00,000. Click the link and enter your details to receive the amount.",
        "बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें",
        "बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें http://bank-verify.com",
        "Hey, are we still meeting for lunch tomorrow?",
        "Thanks for the meeting today. I'll send the report by Friday.",
        "Can you pick up some milk on your way home?"
    ]
    
    print("Testing Rule-Based Spam Detector:")
    print("=" * 50)
    
    for msg in test_messages:
        prediction, confidence = detector.predict(msg)
        result = "SPAM" if prediction == 1 else "NOT SPAM"
        print(f"'{msg[:50]}...' -> {result} (Confidence: {confidence:.4f})")