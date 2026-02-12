from db import engine, Base
from models import User, ChatHistory, Conversation
from sqlalchemy import text

def reset_db_tables():
    print("Resetting database tables...")
    try:
        # Create a connection to execute raw SQL
        with engine.connect() as connection:
            connection.execute(text("COMMIT")) # Ensure no transaction is active
            
            # Drop tables if they exist. Order matters due to foreign keys.
            # ChatHistory depends on Conversation (and User in old schema)
            # Conversation depends on User
            
            print("Dropping chat_history...")
            connection.execute(text("DROP TABLE IF EXISTS chat_history CASCADE"))
            
            print("Dropping conversations...")
            connection.execute(text("DROP TABLE IF EXISTS conversations CASCADE"))
            
            connection.commit()
            
        print("Tables dropped. Re-creating...")
        Base.metadata.create_all(bind=engine)
        print("Database tables re-created successfully.")
        
    except Exception as e:
        print(f"Error resetting tables: {e}")

if __name__ == "__main__":
    reset_db_tables()
