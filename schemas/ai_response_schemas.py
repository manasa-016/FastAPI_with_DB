from pydantic import BaseModel
from typing import Optional

class AIRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant."
    conversation_id: Optional[int] = None

class AIResponse(BaseModel):
    response: str