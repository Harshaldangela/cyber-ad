import requests
import json

def test_extension_functionality():
    """Test the extension functionality by simulating API calls"""
    
    # Test cases
    test_cases = [
        {
            "name": "Spam Message",
            "text": "Make money fast! Double your investment in 24 hours. Click here: http://invest-now.com Limited time offer.",
            "expected_classification": "spam"
        },
        {
            "name": "Normal Message",
            "text": "Hi, how are you doing today? Let's meet for coffee tomorrow.",
            "expected_classification": "not_spam"
        },
        {
            "name": "Phishing Message",
            "text": "Urgent: Your account has been compromised. Click here to verify: http://fake-bank.com/verify",
            "expected_classification": "spam"
        }
    ]
    
    print("Testing Extension Functionality")
    print("=" * 50)
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print(f"Message: {test_case['text']}")
        
        try:
            # Send request to the API
            response = requests.post(
                'http://localhost:8007/analyze',
                json={'text': test_case['text']}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"  Classification: {data.get('classification', 'N/A')}")
                print(f"  Confidence: {data.get('confidence', 0) * 100:.2f}%")
                
                if 'ad' in data:
                    print("  Ad Generated: Yes")
                    print(f"  Ad Content: {data['ad'][:100]}...")
                elif 'ad_generation_error' in data:
                    print(f"  Ad Error: {data['ad_generation_error']}")
                else:
                    print("  Ad Generated: No")
            else:
                print(f"  Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"  Exception: {e}")
            
        print("-" * 30)
    
    print("\nExtension functionality test completed!")

if __name__ == "__main__":
    test_extension_functionality()