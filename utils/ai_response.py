import os
import requests
import time
import random
from dotenv import load_dotenv
from fastapi import HTTPException


def get_completion(user_message, system_message="You are a friendly and helpful AI assistant. Respond naturally and directly to the user’s question in a calm, conversational tone. Avoid introductions, feature lists, promotional language, and unnecessary explanations."):
    """
    Get a completion from the Gemini model using the REST API with exponential backoff retries.
    """
    # Load .env each time so key updates are picked up without restart
    # Load .env explicitly from the project root (parent directory of utils)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    env_path = os.path.join(project_root, ".env")
    
    if os.path.exists(env_path):
        load_dotenv(env_path, override=True)
    else:
        print(f"WARNING: .env file not found at {env_path}")
        load_dotenv(override=True)  # Fallback to default search

    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        api_key = api_key.strip().strip('"').strip("'")
    
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in environment.")
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not found in .env file. Please add it.")

    # Use a more stable model for production
    # Use the more robust 'latest' alias for gemini-1.5-flash
    model = "gemini-1.5-flash-latest"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
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
            print(f"DEBUG: Calling Gemini API (Model: {model}) - Attempt {attempt + 1}")
            response = requests.post(url, headers=headers, json=payload, timeout=50)
            
            # 429 = Rate Limit, 503 = Service Unavailable (High Demand)
            if response.status_code in [429, 503]:
                if attempt < max_retries:
                    delay = (base_delay ** attempt) + random.uniform(0, 1)
                    print(f"WARNING: Gemini API {response.status_code}. Retrying in {delay:.2f}s...")
                    time.sleep(delay)
                    continue
            
            if response.status_code != 200:
                error_text = response.text
                print(f"ERROR: Gemini API returned {response.status_code}: {error_text}")
                
                # Special messages for common errors
                msg = f"AI service unavailable ({response.status_code}). Details: {error_text[:100]}"
                if response.status_code == 429:
                    msg = "Gemini API quota exceeded (429). Please wait a moment."
                elif response.status_code == 404:
                    msg = f"AI Model not found (404). Current model: {model}"
                
                raise HTTPException(status_code=500, detail=msg)

            data = response.json()
            
            # Extract the response text
            if "candidates" in data and len(data["candidates"]) > 0:
                content = data["candidates"][0].get("content", {})
                parts = content.get("parts", [])
                if parts and "text" in parts[0]:
                    print("DEBUG: Gemini API response received successfully.")
                    return parts[0]["text"]
            
            print(f"ERROR: Gemini API unexpected response format: {data}")
            raise Exception("Unexpected response format from Gemini API")
                
        except requests.exceptions.Timeout:
            print("ERROR: Gemini API request timed out.")
            if attempt < max_retries:
                time.sleep(1)
                continue
            raise HTTPException(status_code=504, detail="AI service timed out. Please try again.")
            
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            if status in [429, 503] and attempt < max_retries:
                 time.sleep(2)
                 continue
            msg = "Gemini API quota exceeded (429)." if status == 429 else f"AI service unavailable ({status}). Please try again."
            raise HTTPException(status_code=status if status != 404 else 500, detail=msg)
            
        except Exception as e:
            print(f"ERROR: AI processing error: {str(e)}")
            if attempt < max_retries:
                time.sleep(1)
                continue
            raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")
    
    raise HTTPException(status_code=500, detail="AI processing failed after multiple attempts.")
