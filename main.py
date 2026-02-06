from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
from datetime import datetime
import json

from bot import ChatBot
from models import ChatRequest, ChatResponse, ConversationHistory, SessionInfo

app = FastAPI(title="AI Chatbot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chatbot instances per session
chatbot_sessions: Dict[str, ChatBot] = {}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "websocket": "/ws/{session_id}",
            "history": "/api/history/{session_id}",
            "sessions": "/api/sessions",
            "clear": "/api/clear/{session_id}"
        }
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint with memory and context awareness
    """
    try:
        session_id = request.session_id or "default"
        
        # Create or get chatbot instance for this session
        if session_id not in chatbot_sessions:
            chatbot_sessions[session_id] = ChatBot(session_id=session_id)
        
        chatbot = chatbot_sessions[session_id]
        
        # Get response from chatbot
        response = await chatbot.get_response(
            message=request.message,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return ChatResponse(
            response=response["response"],
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            metadata=response.get("metadata", {})
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history/{session_id}", response_model=ConversationHistory)
async def get_history(session_id: str, limit: Optional[int] = 50):
    """
    Retrieve conversation history for a session
    """
    try:
        if session_id not in chatbot_sessions:
            return ConversationHistory(session_id=session_id, messages=[])
        
        chatbot = chatbot_sessions[session_id]
        history = chatbot.get_history(limit=limit)
        
        return ConversationHistory(
            session_id=session_id,
            messages=history,
            total_messages=len(history)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/clear/{session_id}")
async def clear_history(session_id: str):
    """
    Clear conversation history for a session
    """
    try:
        if session_id in chatbot_sessions:
            chatbot_sessions[session_id].clear_history()
            return {"message": f"History cleared for session {session_id}"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions", response_model=List[SessionInfo])
async def list_sessions():
    """
    List all active chat sessions
    """
    try:
        sessions = []
        for session_id, chatbot in chatbot_sessions.items():
            history = chatbot.get_history(limit=1)
            sessions.append(SessionInfo(
                session_id=session_id,
                created_at=chatbot.created_at,
                message_count=len(chatbot.memory.chat_memory.messages),
                last_message=history[0] if history else None
            ))
        return sessions
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a chat session completely
    """
    try:
        if session_id in chatbot_sessions:
            del chatbot_sessions[session_id]
            return {"message": f"Session {session_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time chat
    """
    await websocket.accept()
    
    # Create or get chatbot instance
    if session_id not in chatbot_sessions:
        chatbot_sessions[session_id] = ChatBot(session_id=session_id)
    
    chatbot = chatbot_sessions[session_id]
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Get response from chatbot
            response = await chatbot.get_response(
                message=message_data.get("message", ""),
                temperature=message_data.get("temperature", 0.7),
                max_tokens=message_data.get("max_tokens", 2000)
            )
            
            # Send response back to client
            await websocket.send_json({
                "response": response["response"],
                "timestamp": datetime.now().isoformat(),
                "metadata": response.get("metadata", {})
            })
    
    except WebSocketDisconnect:
        print(f"Client disconnected from session {session_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "active_sessions": len(chatbot_sessions),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)