import sys
import os
sys.path.append(os.getcwd())
from utils.ai_response import get_completion

try:
    print("Testing AI Completion...")
    response = get_completion("Hi")
    print("-" * 20)
    print("RESPONSE:")
    print(response)
    print("-" * 20)
except Exception as e:
    print(f"FAILED: {e}")
