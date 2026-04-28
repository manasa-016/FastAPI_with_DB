import os
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    api_key = api_key.strip().strip('"').strip("'")

print(f"Testing API Key: {api_key[:10]}...")

model = "gemini-flash-latest"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

headers = {
    "Content-Type": "application/json"
}

payload = {
    "contents": [{
        "parts": [{
            "text": "Hi"
        }]
    }]
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {str(e)}")
