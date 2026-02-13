import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GITHUB_TOKEN")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    data = response.json()
    if 'models' in data:
        print("AVAILABLE MODELS:")
        for model in data['models']:
            print(model['name'])
    else:
        print("No models found or error in response.")
        print(data)
except Exception as e:
    print(f"FAILED: {e}")
