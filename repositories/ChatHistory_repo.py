from models import ChatHistory, Conversation
from sqlalchemy.orm import Session

class ChatHistoryRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, user_id: int, title: str = "New Chat"):
        conversation = Conversation(user_id=user_id, title=title)
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_user_conversations(self, user_id: int):
        return self.db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.created_at.desc()).all()

    def add_chat(self, conversation_id: int, message: str, response: str):
        chat = ChatHistory(conversation_id=conversation_id, message=message, response=response)
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def get_history_by_conversation(self, conversation_id: int):
        return self.db.query(ChatHistory).filter(ChatHistory.conversation_id == conversation_id).order_by(ChatHistory.timestamp.asc()).all()
    
    # Keeping old method for backward compatibility if needed, but updated logic
    def get_history_by_user(self, user_id: int):
        # Fetch all messages for a user across all conversations
        return self.db.query(ChatHistory).join(Conversation).filter(Conversation.user_id == user_id).order_by(ChatHistory.timestamp.desc()).all()
