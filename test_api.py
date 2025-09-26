import requests
import json

# Test the analyze endpoint
url = "http://localhost:8000/analyze"
data = {
    "text": "Congratulations! You've won $1000. Click here to claim your prize now!"
}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error:", str(e))