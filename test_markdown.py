import sys
import os
sys.path.append(os.getcwd())
try:
    from utils.ai_response import get_completion
    # Mocking the schema behavior by passing the system prompt manually for the test
    system_prompt = "You are a helpful and intelligent AI assistant. You always answer in well-structured Markdown format. Use headings, bullet points, bold text, and code blocks where appropriate to make your responses easy to read and professional."
    
    print("Testing AI Completion with Markdown Prompt...")
    response = get_completion("Write a short guide on how to make tea.", system_message=system_prompt)
    print("-" * 20)
    print("RESPONSE:")
    print(response)
    print("-" * 20)
    
except Exception as e:
    print(f"FAILED: {e}")
