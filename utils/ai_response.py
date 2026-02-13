import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

# Gemini REST API Configuration
api_key = os.environ.get("GITHUB_TOKEN") # Reusing the variable name to be consistent with .env
if not api_key:
    api_key = os.environ.get("GOOGLE_API_KEY")

# print(f"DEBUG: Using API Key: {api_key[:10]}... (length: {len(api_key) if api_key else 0})")

def get_completion(user_message, system_message="You are a helpful assistant."):
    """
    Get a completion from the Gemini model using the REST API.
    """
    if not api_key:
        raise Exception("Gemini API key not found in environment variables.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Construct the prompt with system message
    prompt = f"{system_message}\n\nUser: {user_message}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    # print(f"DEBUG: Sending request to Gemini for message: {user_message[:50]}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        # print(f"DEBUG: Gemini response status: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        
        # Extract the response text
        if "candidates" in data and len(data["candidates"]) > 0:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"Gemini API unexpected response format: {data}")
            raise Exception("Unexpected response format from Gemini API")
            
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 429:
            print("ERROR: Gemini API Quota Exceeded (429).")
            raise HTTPException(status_code=429, detail="Gemini API quota exceeded. Please check your API key or wait for the quota to reset.")
        print(f"Gemini REST API Error: {str(e)}")
        if e.response is not None:
             print(f"Response Details: {e.response.text}")
        raise HTTPException(status_code=500, detail="AI processing failed due to API error.")
    except Exception as e:
        print(f"Gemini REST API Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="AI processing failed.")
