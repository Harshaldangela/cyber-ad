import requests
import json

# Test the API with a spam message
response = requests.post(
    'http://localhost:8007/analyze',
    json={
        'text': 'Make money fast! Double your investment in 24 hours. Click here: http://invest-now.com Limited time offer.'
    }
)

print("Status Code:", response.status_code)
print("Response:")
print(json.dumps(response.json(), indent=2))