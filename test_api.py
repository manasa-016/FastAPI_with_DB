import requests
import json

url = "http://127.0.0.1:8000/ai/ask"
payload = {
    "message": "hello",
    "system_prompt": "You are a helpful assistant."
}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {str(e)}")
