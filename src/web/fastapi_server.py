"""
FastAPI Backend Server - REST API for AI Chat Bot
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

from src.core.chat_engine import AIChatEngine
from src.utils.config_loader import load_config

# Pydantic models for request/response
class ChatMessage(BaseModel):
    message: str
    user_id: str = "default"
    conversation_mode: str = "default"
    temperature: float = 0.7
    max_tokens: int = 500

class ChatResponse(BaseModel):
    success: bool
    response: str
    usage: Optional[dict] = None
    model: Optional[str] = None
    conversation_length: Optional[int] = None
    error: Optional[str] = None

class ConversationStats(BaseModel):
    total_messages: int
    user_messages: int
    assistant_messages: int
    api_usage: dict

# Initialize FastAPI app
app = FastAPI(
    title="AI Chat Bot API",
    description="REST API for AI-powered chat assistant",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chat engine instance
chat_engine = None

@app.on_event("startup")
async def startup_event():
    """Initialize chat engine on startup"""
    global chat_engine
    try:
        config = load_config()
        chat_engine = AIChatEngine(
            api_key=config['openai_api_key'],
            model=config.get('model', 'gpt-3.5-turbo')
        )
        print("✅ AI Chat Engine initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize AI Chat Engine: {e}")
        raise e

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Chat Bot API",
        "status": "running",
        "version": "1.0.0"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """Main chat endpoint"""
    if chat_engine is None:
        raise HTTPException(status_code=503, detail="Chat engine not initialized")
    
    try:
        result = chat_engine.chat(
            message=chat_message.message,
            user_id=chat_message.user_id,
            conversation_mode=chat_message.conversation_mode,
            temperature=chat_message.temperature,
            max_tokens=chat_message.max_tokens
        )
        
        if result["success"]:
            return ChatResponse(**result)
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversation/{user_id}/stats")
async def get_conversation_stats(user_id: str):
    """Get conversation statistics"""
    if chat_engine is None:
        raise HTTPException(status_code=503, detail="Chat engine not initialized")
    
    try:
        stats = chat_engine.get_conversation_stats(user_id)
        return ConversationStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/conversation/{user_id}")
async def clear_conversation(user_id: str):
    """Clear conversation history"""
    if chat_engine is None:
        raise HTTPException(status_code=503, detail="Chat engine not initialized")
    
    try:
        chat_engine.memory.clear_conversation(user_id)
        return {"message": f"Conversation cleared for user {user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "chat_engine_ready": chat_engine is not None
    }

if __name__ == "__main__":
    uvicorn.run(
        "src.web.fastapi_server:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )