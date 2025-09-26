import requests
import json

# Test messages that were previously failing
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
    "बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें http://bank-verify.com"
]

url = "http://localhost:8000/analyze"

print("Testing Enhanced Spam Classifier API")
print("=" * 50)

for i, message in enumerate(test_messages, 1):
    try:
        response = requests.post(url, json={"text": message})
        if response.status_code == 200:
            result = response.json()
            classification = result.get("classification", "unknown")
            confidence = result.get("confidence", 0)
            print(f"{i:2d}. {message[:50]}...")
            print(f"    Classification: {classification.upper()} (Confidence: {confidence:.4f})")
            if "ad" in result:
                print(f"    Ad Generated: Yes")
            print()
        else:
            print(f"{i:2d}. Error: Status code {response.status_code}")
            print()
    except Exception as e:
        print(f"{i:2d}. Error: {str(e)}")
        print()

print("Test completed!")