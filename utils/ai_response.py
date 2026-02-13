import os
import requests
import time
import random
from dotenv import load_dotenv
from fastapi import HTTPException


def get_completion(user_message, system_message="You are a helpful assistant."):
    """
    Get a completion from the Gemini model using the REST API with exponential backoff retries.
    """
    # Load .env each time so key updates are picked up without restart
    load_dotenv(override=True)
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        api_key = api_key.strip().strip('"').strip("'")
    
    if not api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not found in .env file. Please add it.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
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
    
    max_retries = 3
    base_delay = 2  # seconds

    for attempt in range(max_retries + 1):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 429:
                if attempt < max_retries:
                    # Exponential backoff with jitter
                    delay = (base_delay ** attempt) + random.uniform(0, 1)
                    print(f"WARNING: Gemini API Quota Exceeded (429). Retrying in {delay:.2f}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                    continue
                else:
                    print("ERROR: Gemini API Quota Exceeded (429) after max retries.")
                    raise HTTPException(status_code=429, detail="Gemini API quota exceeded. Please check your API key or wait for the quota to reset.")
            
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
                 # Already handled above, but just in case
                 if attempt < max_retries:
                     continue
                 raise HTTPException(status_code=429, detail="Gemini API quota exceeded.")
            
            print(f"Gemini REST API Error: {str(e)}")
            if e.response is not None:
                 print(f"Response Details: {e.response.text}")
                 raise HTTPException(status_code=500, detail=f"AI processing failed due to API error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=500, detail="AI processing failed due to API error (No response body).")
        except Exception as e:
            print(f"Gemini REST API Error: {str(e)}")
            import traceback
            traceback.print_exc()
            if attempt < max_retries:
                time.sleep(1)
                continue
            raise HTTPException(status_code=500, detail=f"AI processing failed after retries: {str(e)}")
    
    raise HTTPException(status_code=500, detail="AI processing failed after multiple attempts.")
