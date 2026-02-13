import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_conversation_flow():
    print("\n--- Testing Conversation Flow ---")
    
    # 1. Login
    login_url = f"{BASE_URL}/login"
    user_data = {"email": "testuser@example.com", "password": "password123"}
    
    # Ensure user exists
    requests.post(f"{BASE_URL}/signup", json=user_data)
    
    login_resp = requests.post(login_url, json=user_data)
    if login_resp.status_code != 200:
        print(f"Login failed: {login_resp.text}")
        return

    token = login_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Ask (Should create a new conversation implicitly)
    ask_url = f"{BASE_URL}/ai/ask"
    payload = {"message": "start a new conversation"}
    resp1 = requests.post(ask_url, json=payload, headers=headers)
    print(f"Msg 1 Status: {resp1.status_code}")
    if resp1.status_code != 200:
        print(f"Msg 1 Error Detail: {resp1.text}")
        return
    print(f"Msg 1 Response: {resp1.json().get('response')[:30]}...")
    
    # 3. Ask again (Should ideally continue if we passed conversation_id, but here it might create new one or just log)
    # The current implementation creates a NEW conversation if conversation_id is missing.
    payload2 = {"message": "second message in new conversation"}
    resp2 = requests.post(ask_url, json=payload2, headers=headers)
    print(f"Msg 2 Status: {resp2.status_code}")
    
    # 4. Fetch History
    history_url = f"{BASE_URL}/ai/history"
    hist_resp = requests.get(history_url, headers=headers)
    print(f"History Status: {hist_resp.status_code}")
    history = hist_resp.json().get("history", [])
    print(f"Total History Items: {len(history)}")
    if len(history) > 0:
        first = history[0]
        print(f"Latest Item ID: {first.get('id')}")
        print(f"Latest Item Conversation ID: {first.get('conversation_id')}")

if __name__ == "__main__":
    try:
        test_conversation_flow()
    except Exception as e:
        print(f"Test failed: {e}")
