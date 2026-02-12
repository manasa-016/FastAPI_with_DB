from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from db import get_db
from utils.ai_response import get_completion
from utils.jwt_handler import verify_token
from schemas.ai_response_schemas import AIRequest, AIResponse
from schemas.chat_schemas import ChatHistoryList, ChatHistoryResponse
from repositories.ChatHistory_repo import ChatHistoryRepo
from typing import Optional

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/ask", response_model=AIResponse)
async def ask_ai(
    request: AIRequest, 
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get response from AI model asynchronously. Saves history if user is logged in."""
    user_id = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        if payload:
            user_id = int(payload.get("sub"))

    try:
        response = await run_in_threadpool(
            get_completion, 
            request.message, 
            request.system_prompt
        )
        
        # Save history only if logged in
        if user_id:
            repo = ChatHistoryRepo(db)
            repo.add_chat(user_id, request.message, response)
            
        return AIResponse(response=response)
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="AI processing failed.")

@router.get("/history", response_model=ChatHistoryList)
def get_ai_history(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """Fetch chat history for the logged-in user."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token type")
        
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    user_id = int(payload.get("sub"))
    repo = ChatHistoryRepo(db)
    history = repo.get_history_by_user(user_id)
    
    return ChatHistoryList(history=history)