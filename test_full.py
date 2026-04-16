import requests
import json

base_url = "http://127.0.0.1:8000"

# 1. Login
print("Logging in...")
login_res = requests.post(f"{base_url}/login", json={
    "email": "qwertq@gmail.com",
    "password": "123456"
})
if login_res.status_code != 200:
    print(f"Login failed: {login_res.text}")
    exit(1)

token = login_res.json()["access_token"]
print("Login successful.")

# 2. Ask AI
print("Asking AI...")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
payload = {
    "message": "Verify that everything is working now.",
    "system_prompt": "Respond with 'SYSTEM READY' if you can hear me."
}

try:
    response = requests.post(f"{base_url}/ai/ask", headers=headers, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {str(e)}")
