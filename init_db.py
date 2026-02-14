from db import engine, Base
from models import User, ChatHistory, Conversation # Import all models to ensure they are registered

def init_db():
    print("Initializing database...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    init_db()
