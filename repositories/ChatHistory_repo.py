from models import ChatHistory
from sqlalchemy.orm import Session

class ChatHistoryRepo:
    def __init__(self, db: Session):
        self.db = db

    def add_chat(self, user_id: int, message: str, response: str):
        chat = ChatHistory(user_id=user_id, message=message, response=response)
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def get_history_by_user(self, user_id: int):
        return self.db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.timestamp.desc()).all()
