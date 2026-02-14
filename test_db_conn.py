from db import engine, SessionLocal
from sqlalchemy import inspect
from models import Base

def test_conn():
    try:
        print("Checking tables in database...")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables found: {tables}")
        
        required_tables = ["users", "conversations", "chat_history"]
        for table in required_tables:
            if table in tables:
                print(f"✅ Table '{table}' exists.")
            else:
                print(f"❌ Table '{table}' MISSING!")
        
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ Database connection successful.")
        db.close()
    except Exception as e:
        print(f"❌ Database connection FAILED: {e}")

if __name__ == "__main__":
    test_conn()
