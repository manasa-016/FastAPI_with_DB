from pydantic import BaseModel
from datetime import datetime
from typing import List

class ChatHistoryBase(BaseModel):
    message: str
    response: str
    timestamp: datetime

class ChatHistoryResponse(ChatHistoryBase):
    id: int
    conversation_id: int

    class Config:
        from_attributes = True

class ChatHistoryList(BaseModel):
    history: List[ChatHistoryResponse]
