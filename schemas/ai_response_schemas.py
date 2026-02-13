from pydantic import BaseModel
from typing import Optional

class AIRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful and intelligent AI assistant. You always answer in well-structured Markdown format. Use headings, bullet points, bold text, and code blocks where appropriate to make your responses easy to read and professional."
    conversation_id: Optional[int] = None

class AIResponse(BaseModel):
    response: str
    conversation_id: Optional[int] = None
