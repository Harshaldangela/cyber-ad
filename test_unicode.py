import requests
import json

text = 'बधाई हो! आपने ₹10,00,000 जीते हैं। राशि पाने के लिए लिंक पर क्लिक करें और अपना विवरण दर्ज करें'
data = {'text': text}

print('Sending:', json.dumps(data, ensure_ascii=False))

response = requests.post('http://127.0.0.1:8006/test-detection', json=data)
print('Status:', response.status_code)
print('Response:', response.json())