from pydantic import BaseModel
from typing import Optional

class AIRequest(BaseModel):
    message: str
    system_prompt: str = "You are a friendly and helpful AI assistant. Respond naturally and directly to the user’s question in a calm, conversational tone. Avoid introductions, feature lists, promotional language, and unnecessary explanations."
    conversation_id: Optional[int] = None

class AIResponse(BaseModel):
    response: str
    conversation_id: Optional[int] = None
