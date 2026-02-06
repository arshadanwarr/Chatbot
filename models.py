from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(default="default", description="Session ID for conversation tracking")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=1.0, description="Model temperature")
    max_tokens: Optional[int] = Field(default=2000, ge=1, le=4096, description="Maximum tokens in response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello, how are you?",
                "session_id": "user123",
                "temperature": 0.7,
                "max_tokens": 2000
            }
        }

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="Bot response")
    session_id: str = Field(..., description="Session ID")
    timestamp: str = Field(..., description="Response timestamp")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional metadata")

class Message(BaseModel):
    """Individual message in conversation"""
    role: str = Field(..., description="Message role: user or assistant")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="Message timestamp")

class ConversationHistory(BaseModel):
    """Conversation history response"""
    session_id: str = Field(..., description="Session ID")
    messages: List[Message] = Field(..., description="List of messages")
    total_messages: Optional[int] = Field(default=0, description="Total message count")

class SessionInfo(BaseModel):
    """Session information"""
    session_id: str = Field(..., description="Session ID")
    created_at: str = Field(..., description="Session creation timestamp")
    message_count: int = Field(..., description="Number of messages in session")
    last_message: Optional[Message] = Field(default=None, description="Last message in conversation")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())