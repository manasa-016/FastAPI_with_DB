from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.ai_response_routes import router as ai_response_router
from routes.email_routes import router as email_router
from db import get_db, engine
from fastapi.middleware.cors import CORSMiddleware
from models import Base
import os


app = FastAPI()

@app.on_event("startup")
def startup_event():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialization complete.")

# Database initialization should be handled externally or as a migration
# If you want it on startup, run it as a background task to avoid blocking the server.

#cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173", 
        "http://localhost:3000",
        "https://lumina-black-eta.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(ai_response_router)
app.include_router(email_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test-ai")
async def test_ai():
    from utils.ai_response import get_completion
    try:
        response = get_completion("Hi")
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Use PORT environment variable for Render compatibility
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)