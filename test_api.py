import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "AI Chatbot API"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "active_sessions" in response.json()

def test_chat_endpoint():
    """Test chat endpoint"""
    response = client.post(
        "/api/chat",
        json={
            "message": "Hello, how are you?",
            "session_id": "test-session",
            "temperature": 0.7,
            "max_tokens": 100
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "session_id" in data
    assert data["session_id"] == "test-session"

def test_get_history():
    """Test getting conversation history"""
    # First send a message
    client.post(
        "/api/chat",
        json={
            "message": "Test message",
            "session_id": "history-test"
        }
    )
    
    # Then get history
    response = client.get("/api/history/history-test")
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data
    assert data["session_id"] == "history-test"

def test_clear_history():
    """Test clearing conversation history"""
    # Create a session with a message
    client.post(
        "/api/chat",
        json={
            "message": "Test message",
            "session_id": "clear-test"
        }
    )
    
    # Clear history
    response = client.delete("/api/clear/clear-test")
    assert response.status_code == 200
    assert "message" in response.json()

def test_list_sessions():
    """Test listing all sessions"""
    # Create a session
    client.post(
        "/api/chat",
        json={
            "message": "Test",
            "session_id": "session-list-test"
        }
    )
    
    # List sessions
    response = client.get("/api/sessions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_session():
    """Test deleting a session"""
    # Create a session
    client.post(
        "/api/chat",
        json={
            "message": "Test",
            "session_id": "delete-test"
        }
    )
    
    # Delete session
    response = client.delete("/api/sessions/delete-test")
    assert response.status_code == 200

def test_invalid_session_history():
    """Test getting history for non-existent session"""
    response = client.get("/api/history/non-existent-session")
    assert response.status_code == 200
    data = response.json()
    assert data["messages"] == []

def test_chat_with_custom_temperature():
    """Test chat with different temperature values"""
    response = client.post(
        "/api/chat",
        json={
            "message": "Generate creative text",
            "session_id": "temp-test",
            "temperature": 0.9
        }
    )
    assert response.status_code == 200

def test_chat_validation():
    """Test chat endpoint validation"""
    # Missing message
    response = client.post(
        "/api/chat",
        json={
            "session_id": "validation-test"
        }
    )
    assert response.status_code == 422  # Validation error

if __name__ == "__main__":
    pytest.main([__file__, "-v"])